import unittest

from node import parse_message, reduce_state, PeerState, to_millis


class NodeDeterminismTests(unittest.TestCase):
    def test_parse_message_requires_schema(self):
        self.assertIsNone(parse_message("swarm/state", '{"type":"HEARTBEAT","peer_id":"a"}'))

        parsed = parse_message(
            "swarm/state",
            '{"type":"HEARTBEAT","peer_id":"a","ts":1710000000}',
        )
        self.assertEqual(parsed["type"], "HEARTBEAT")
        self.assertEqual(parsed["peer_id"], "a")
        self.assertEqual(parsed["ts"], 1710000000)

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


if __name__ == "__main__":
    unittest.main()
