import unittest
import json

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
)


class NodeDeterminismTests(unittest.TestCase):
    def setUp(self):
        RECENT_MESSAGE_HASHES.clear()
        RECENT_MESSAGE_HASHES_SET.clear()

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


if __name__ == "__main__":
    unittest.main()
