import unittest
import json
from copy import deepcopy

from node import (
    parse_message,
    reduce_state,
    PeerState,
    to_millis,
    apply_stale_detection,
    STALE_THRESHOLD_MS,
    sign_payload,
    seen_recently,
    RECENT_MESSAGE_HASHES,
    RECENT_MESSAGE_HASHES_SET,
    append_proof_log,
    PROOF_LOG,
    TaskRequirements,
    TaskSpec,
    assign_task,
    create_task_record,
    rebalance_recoverable_tasks,
    handle_task_result,
    TASKS,
    TASK_ASSIGNED,
    TASK_COMPLETED,
    TASK_RECOVERABLE,
    TASK_SECURE,
)


class NodeDeterminismTests(unittest.TestCase):
    def setUp(self):
        RECENT_MESSAGE_HASHES.clear()
        RECENT_MESSAGE_HASHES_SET.clear()
        PROOF_LOG.clear()
        TASKS.clear()

    def test_parse_message_requires_schema(self):
        invalid_schema = {"payload": {"type": "HEARTBEAT", "peer_id": "a"}, "sig": "x"}
        self.assertIsNone(parse_message("swarm/state", json.dumps(invalid_schema)))

        payload = {"type": "HEARTBEAT", "peer_id": "a", "ts": 1710000000}
        signed = {"payload": payload, "sig": sign_payload(payload)}
        parsed = parse_message("swarm/state", json.dumps(signed))
        self.assertEqual(parsed["type"], "HEARTBEAT")
        self.assertEqual(parsed["peer_id"], "a")
        self.assertEqual(parsed["ts"], 1710000000)

    def test_tampered_messages_are_rejected(self):
        payload = {"type": "HEARTBEAT", "peer_id": "a", "ts": 1710000000}
        signed = {"payload": payload, "sig": sign_payload(payload)}
        tampered = {"payload": {**payload, "peer_id": "evil"}, "sig": signed["sig"]}
        self.assertIsNone(parse_message("swarm/state", json.dumps(tampered)))

    def test_signature_uses_shared_secret_authentication(self):
        payload = {"type": "HEARTBEAT", "peer_id": "a", "ts": 1710000000}
        bad_sig = "0" * 64
        forged = {"payload": payload, "sig": bad_sig}
        self.assertIsNone(parse_message("swarm/state", json.dumps(forged)))

    def test_to_millis_normalizes_seconds_and_millis(self):
        self.assertEqual(to_millis(1710000000), 1710000000000)
        self.assertEqual(to_millis(1710000000000), 1710000000000)

    def test_reduce_state_drops_delayed_messages(self):
        prev = PeerState(peer_id="agent_a", last_seen_ms=1710000002000, role="worker", status="ready")
        delayed_event = {"type": "HEARTBEAT", "peer_id": "agent_a", "ts": 1710000001}
        self.assertIsNone(reduce_state(prev, delayed_event))

    def test_reduce_state_accepts_equal_or_newer_timestamps(self):
        prev = PeerState(peer_id="agent_a", last_seen_ms=1710000001000, role="worker", status="ready")
        equal_event = {"type": "HEARTBEAT", "peer_id": "agent_a", "ts": 1710000001}
        newer_event = {"type": "HEARTBEAT", "peer_id": "agent_a", "ts": 1710000002, "role": "leader"}

        equal_state = reduce_state(prev, equal_event)
        self.assertIsNotNone(equal_state)
        self.assertEqual(equal_state.last_seen_ms, 1710000001000)

        newer_state = reduce_state(equal_state, newer_event)
        self.assertIsNotNone(newer_state)
        self.assertEqual(newer_state.last_seen_ms, 1710000002000)
        self.assertEqual(newer_state.role, "leader")

    def test_replay_cache_detects_repeated_event(self):
        event = {"type": "HEARTBEAT", "peer_id": "agent_a", "ts": 1710000000}
        self.assertFalse(seen_recently(event))
        self.assertTrue(seen_recently(event))

    def test_stale_detection_marks_dead_node(self):
        state = {
            "agent_a": PeerState(peer_id="agent_a", last_seen_ms=1000, role="worker", status="ready"),
            "agent_b": PeerState(peer_id="agent_b", last_seen_ms=8000, role="worker", status="ready"),
        }
        changed = apply_stale_detection(state, now_ms_value=1000 + STALE_THRESHOLD_MS + 1)
        self.assertTrue(changed)
        self.assertEqual(state["agent_a"].status, "stale")
        self.assertEqual(state["agent_b"].status, "ready")

    def test_role_assignment_is_lexicographic_for_ready_peers(self):
        state = {
            "agent_b": PeerState(peer_id="agent_b", last_seen_ms=10_000, role="worker", status="ready"),
            "agent_a": PeerState(peer_id="agent_a", last_seen_ms=10_000, role="worker", status="ready"),
            "agent_c": PeerState(peer_id="agent_c", last_seen_ms=0, role="worker", status="ready"),
        }

        # make agent_c stale, ensure leader is the smallest READY peer id
        apply_stale_detection(state, now_ms_value=STALE_THRESHOLD_MS + 1)
        self.assertEqual(state["agent_c"].status, "stale")
        self.assertEqual(state["agent_a"].role, "leader")
        self.assertEqual(state["agent_b"].role, "worker")

        # if agent_a later becomes stale, leadership should move to agent_b
        state["agent_b"].last_seen_ms = 20_000
        apply_stale_detection(state, now_ms_value=10_000 + STALE_THRESHOLD_MS + 1)
        self.assertEqual(state["agent_a"].status, "stale")
        self.assertEqual(state["agent_b"].role, "leader")

    def test_proof_log_appends_event_with_required_fields(self):
        append_proof_log("STATE_TRANSITION", "agent_a", 1710000000, {"source_type": "HEARTBEAT"})
        self.assertEqual(len(PROOF_LOG), 1)
        record = PROOF_LOG[0]
        self.assertIn("event_id", record)
        self.assertEqual(record["type"], "STATE_TRANSITION")
        self.assertEqual(record["peer_id"], "agent_a")
        self.assertEqual(record["ts"], 1710000000)

    def test_task_assignment_deterministic_with_50_agents(self):
        state_a = {
            f"agent_{i:02d}": PeerState(peer_id=f"agent_{i:02d}", last_seen_ms=10_000, role="worker", status="ready")
            for i in range(50)
        }
        state_a["agent_00"].role = "leader"
        state_b = deepcopy(state_a)

        fast = TaskSpec("T_FAST", "FAST_TASK", TaskRequirements(1, "worker", 1000, 1), {})
        secure = TaskSpec("T_SEC", TASK_SECURE, TaskRequirements(2, "any", 1000, 3), {})
        recoverable = TaskSpec("T_REC", TASK_RECOVERABLE, TaskRequirements(1, "any", 1000, 1), {})

        self.assertEqual(assign_task(fast, state_a), assign_task(fast, state_b))
        self.assertEqual(assign_task(secure, state_a), assign_task(secure, state_b))
        self.assertEqual(assign_task(recoverable, state_a), assign_task(recoverable, state_b))

    def test_recoverable_task_reassigns_when_assignee_stale(self):
        state = {
            f"agent_{i:02d}": PeerState(peer_id=f"agent_{i:02d}", last_seen_ms=10_000, role="worker", status="ready")
            for i in range(50)
        }
        task = TaskSpec("T_REC_1", TASK_RECOVERABLE, TaskRequirements(1, "any", 1000, 1), {})
        TASKS[task.task_id] = create_task_record(task, state)
        first_assignee = TASKS[task.task_id]["assignees"][0]
        state[first_assignee].status = "stale"

        rebalance_recoverable_tasks(state)

        self.assertEqual(TASKS[task.task_id]["state"], TASK_ASSIGNED)
        self.assertNotEqual(TASKS[task.task_id]["assignees"][0], first_assignee)

    def test_secure_task_results_must_match(self):
        state = {
            f"agent_{i:02d}": PeerState(peer_id=f"agent_{i:02d}", last_seen_ms=10_000, role="worker", status="ready")
            for i in range(50)
        }
        task = TaskSpec("T_SEC_1", TASK_SECURE, TaskRequirements(2, "any", 1000, 2), {})
        TASKS[task.task_id] = create_task_record(task, state)
        assignee_a, assignee_b = TASKS[task.task_id]["assignees"]

        self.assertTrue(handle_task_result({"task_id": task.task_id, "peer_id": assignee_a, "result": "OK", "ts": 1}))
        self.assertFalse(handle_task_result({"task_id": task.task_id, "peer_id": assignee_b, "result": "DIFF", "ts": 2}))
        self.assertEqual(TASKS[task.task_id]["state"], TASK_ASSIGNED)

        self.assertTrue(handle_task_result({"task_id": task.task_id, "peer_id": assignee_a, "result": "OK", "ts": 3}))
        self.assertTrue(handle_task_result({"task_id": task.task_id, "peer_id": assignee_b, "result": "OK", "ts": 4}))
        self.assertEqual(TASKS[task.task_id]["state"], TASK_COMPLETED)

    def test_fault_injection_stream_consistency_with_50_agents(self):
        def build_state():
            return {
                f"agent_{i:02d}": PeerState(peer_id=f"agent_{i:02d}", last_seen_ms=10_000, role="worker", status="ready")
                for i in range(50)
            }

        stream = [
            {"type": "HEARTBEAT", "peer_id": "agent_10", "ts": 11},
            {"type": "HEARTBEAT", "peer_id": "agent_10", "ts": 11},  # replay
            {"type": "HEARTBEAT", "peer_id": "agent_10", "ts": 10},  # delayed/old
            {"type": "HEARTBEAT", "peer_id": "agent_20", "ts": 12},
        ]

        state_a = build_state()
        state_b = build_state()
        for state in (state_a, state_b):
            RECENT_MESSAGE_HASHES.clear()
            RECENT_MESSAGE_HASHES_SET.clear()
            for event in stream:
                if seen_recently(event):
                    continue
                prev = state.get(event["peer_id"])
                next_state = reduce_state(prev, event)
                if next_state is not None:
                    state[event["peer_id"]] = next_state

            # simulate "kill process" effect for one peer via stale detection window
            state["agent_49"].last_seen_ms = 0
            apply_stale_detection(state, now_ms_value=STALE_THRESHOLD_MS + 1)

        snapshot_a = {k: (v.last_seen_ms, v.role, v.status) for k, v in sorted(state_a.items())}
        snapshot_b = {k: (v.last_seen_ms, v.role, v.status) for k, v in sorted(state_b.items())}
        self.assertEqual(snapshot_a, snapshot_b)
        self.assertEqual(state_a["agent_49"].status, "stale")


if __name__ == "__main__":
    unittest.main()
