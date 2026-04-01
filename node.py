"""
Tashi FoxMQ Warmup — The Stateful Handshake
Starter skeleton for participants.

FoxMQ is a Byzantine fault-tolerant MQTT 5.0 broker powered by Vertex consensus.
Any standard MQTT client library works against it — messages are consensus-ordered
before delivery, so all subscribers always see the same event order.

This script connects to a local FoxMQ node and:
  - Connects with credentials
  - Subscribes to the swarm topic
  - Publishes a raw HELLO message so you can see it arrive on the other side

Your job is to extend this into the full Stateful Handshake challenge.

Pre-requisites:
    1. FoxMQ broker running locally (see setup steps below or README)
    2. Python 3.8+
    3. pip install -r requirements.txt

Usage:
    python node.py --host 127.0.0.1 --port 1883 \\
                   --username agent_a --password secret \\
                   --agent-id agent_a
"""

import argparse
import json
import time
import threading
from dataclasses import dataclass, asdict
from typing import Dict, Optional
import paho.mqtt.client as mqtt

# ---------------------------------------------------------------------------
# Topics — you are free to add more
# ---------------------------------------------------------------------------
TOPIC_SWARM = "swarm/state"      # shared BFT-ordered state topic
TOPIC_HELLO = "swarm/hello"      # initial handshake topic

# ---------------------------------------------------------------------------
# TODO: Define your shared state here.
#
# The warm-up requires each agent to maintain a replicated state like:
#   {
#     "peer_id":      str,
#     "last_seen_ms": int,    # epoch milliseconds
#     "role":         str,    # e.g. "scout" | "carrier"
#     "status":       str,    # e.g. "ready" | "busy" | "stale"
#   }
#
# Since FoxMQ uses Vertex under the hood, all subscribers receive messages in
# the SAME consensus-ordered sequence — so your local state will always match
# every other agent's local state if your update logic is deterministic.
# ---------------------------------------------------------------------------
@dataclass
class PeerState:
    peer_id: str
    last_seen_ms: int
    role: str
    status: str


STATE: Dict[str, PeerState] = {}
STATE_LOCK = threading.Lock()

RECV_ORDER_INDEX = 0
RECV_ORDER_LOCK = threading.Lock()


def next_recv_order_index() -> int:
    global RECV_ORDER_INDEX
    with RECV_ORDER_LOCK:
        RECV_ORDER_INDEX += 1
        return RECV_ORDER_INDEX


def parse_message(topic: str, payload: str) -> Optional[dict]:
    """Parse inbound JSON and normalize to a structured event dict."""
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        print(f"[WARN] Ignoring non-JSON message on topic={topic}")
        return None

    if not isinstance(data, dict):
        print(f"[WARN] Ignoring non-object message on topic={topic}")
        return None

    message_type = data.get("type")
    peer_id = data.get("peer_id")
    if not isinstance(message_type, str) or not isinstance(peer_id, str):
        print(f"[WARN] Missing/invalid type or peer_id on topic={topic}")
        return None

    return {
        "type": message_type,
        "peer_id": peer_id,
        "ts": data.get("ts"),
        "last_seen_ms": data.get("last_seen_ms"),
        "role": data.get("role"),
        "status": data.get("status"),
    }


def reduce_state(previous: Optional[PeerState], event: dict) -> PeerState:
    """
    Deterministic state transition:
      - purely computed from previous state + input event
      - no randomness / no wall-clock dependency
    """
    peer_id = event["peer_id"]
    baseline = previous or PeerState(
        peer_id=peer_id,
        last_seen_ms=0,
        role="worker",
        status="ready",
    )

    event_last_seen_ms = event.get("last_seen_ms")
    if not isinstance(event_last_seen_ms, int):
        ts = event.get("ts")
        if isinstance(ts, int):
            # HELLO uses seconds in Issue 1, normalize to ms for replicated state.
            event_last_seen_ms = ts * 1000
        else:
            event_last_seen_ms = baseline.last_seen_ms

    role = event.get("role") if isinstance(event.get("role"), str) else baseline.role
    status = event.get("status") if isinstance(event.get("status"), str) else baseline.status

    return PeerState(
        peer_id=peer_id,
        last_seen_ms=event_last_seen_ms,
        role=role,
        status=status,
    )


def on_connect(client: mqtt.Client, userdata, flags, reason_code, properties):
    """Called when the client connects to the FoxMQ broker."""
    if reason_code == 0:
        print(f"[CONNECTED] broker={userdata['host']}:{userdata['port']}")

        # Subscribe to the shared swarm topics
        client.subscribe(TOPIC_SWARM, qos=1)
        client.subscribe(TOPIC_HELLO, qos=1)
        print(f"[SUBSCRIBED] {TOPIC_SWARM}, {TOPIC_HELLO}")

        hello = {
            "type": "HELLO",
            "peer_id": userdata["agent_id"],
            "ts": int(time.time()),
        }
        publish_json(client, TOPIC_HELLO, hello)
        # TODO: start a background heartbeat thread

    else:
        print(f"[ERROR] Connection failed: {reason_code}")


def on_message(client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
    """Called for every consensus-ordered message that arrives from FoxMQ."""
    topic = message.topic
    payload = message.payload.decode("utf-8")
    recv_order_index = next_recv_order_index()

    print(f"[RECV] idx={recv_order_index} topic={topic} payload={payload}")

    event = parse_message(topic, payload)
    if event is None:
        return

    with STATE_LOCK:
        prev = STATE.get(event["peer_id"])
        STATE[event["peer_id"]] = reduce_state(prev, event)
        snapshot = {k: asdict(v) for k, v in sorted(STATE.items(), key=lambda item: item[0])}
    print(f"[STATE] {json.dumps(snapshot, sort_keys=True)}")

    # TODO: detect stale peers (check last_seen_ms against current time)
    # TODO: mirror role changes from peers


def on_disconnect(client: mqtt.Client, userdata, flags, reason_code, properties):
    print(f"[DISCONNECTED] reason={reason_code}")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def now_ms() -> int:
    return int(time.time() * 1000)


def publish_json(client: mqtt.Client, topic: str, data: dict) -> None:
    """Publish a dict as a JSON message with QoS 1."""
    payload = json.dumps(data)
    client.publish(topic, payload, qos=1)
    print(f"[SEND] topic={topic}  payload={payload}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="FoxMQ Warmup – Stateful Handshake")
    parser.add_argument("--host",     default="127.0.0.1", help="FoxMQ broker host")
    parser.add_argument("--port",     default=1883, type=int, help="FoxMQ broker MQTT port")
    parser.add_argument("--username", required=True, help="FoxMQ username")
    parser.add_argument("--password", required=True, help="FoxMQ password")
    parser.add_argument("--agent-id", required=True, help="Unique ID for this agent")
    args = parser.parse_args()

    # Build MQTTv5 client
    client = mqtt.Client(
        client_id=args.agent_id,
        protocol=mqtt.MQTTv5,
        userdata={"host": args.host, "port": args.port, "agent_id": args.agent_id},
    )

    client.username_pw_set(args.username, args.password)
    client.on_connect    = on_connect
    client.on_message    = on_message
    client.on_disconnect = on_disconnect

    print(f"[INFO] Connecting to FoxMQ at {args.host}:{args.port} as {args.agent_id}")
    client.connect(args.host, args.port, keepalive=60)

    # Blocking network loop — handles reconnects automatically
    client.loop_forever()


if __name__ == "__main__":
    main()
