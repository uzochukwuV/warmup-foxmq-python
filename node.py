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
import hashlib
import hmac
import json
import os
import time
import threading
from collections import deque
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional
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


@dataclass
class TaskRequirements:
    min_agents: int
    required_role: str
    max_latency_ms: int
    redundancy: int


@dataclass
class TaskSpec:
    task_id: str
    type: str
    requirements: TaskRequirements
    payload: Dict[str, Any]


STATE: Dict[str, PeerState] = {}
STATE_LOCK = threading.Lock()

RECV_ORDER_INDEX = 0
RECV_ORDER_LOCK = threading.Lock()
HEARTBEAT_INTERVAL_SEC = 2
STALE_CHECK_INTERVAL_SEC = 1
STALE_THRESHOLD_MS = 5000
RECENT_HASH_CACHE_SIZE = 256
RECENT_MESSAGE_HASHES = deque(maxlen=RECENT_HASH_CACHE_SIZE)
RECENT_MESSAGE_HASHES_SET = set()
PROOF_LOG = []
PROOF_LOG_LOCK = threading.Lock()
SIGNING_SECRET = os.environ.get("SWARM_SIGNING_SECRET", "vertex-swarm-shared-secret")
TASKS: Dict[str, dict] = {}
TASKS_LOCK = threading.Lock()

TASK_CREATED = "CREATED"
TASK_ASSIGNED = "ASSIGNED"
TASK_EXECUTING = "EXECUTING"
TASK_COMPLETED = "COMPLETED"

TASK_FAST = "FAST_TASK"
TASK_SECURE = "SECURE_TASK"
TASK_RECOVERABLE = "RECOVERABLE_TASK"


def next_recv_order_index() -> int:
    global RECV_ORDER_INDEX
    with RECV_ORDER_LOCK:
        RECV_ORDER_INDEX += 1
        return RECV_ORDER_INDEX


def canonical_json(data: dict) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sign_payload(payload: dict) -> str:
    mac = hmac.new(
        SIGNING_SECRET.encode("utf-8"),
        canonical_json(payload).encode("utf-8"),
        hashlib.sha256,
    )
    return mac.hexdigest()


def verify_envelope(envelope: dict) -> bool:
    payload = envelope.get("payload")
    sig = envelope.get("sig")
    if not isinstance(payload, dict) or not isinstance(sig, str):
        return False
    expected_sig = sign_payload(payload)
    return sig == expected_sig


def parse_message(topic: str, raw_message: str) -> Optional[dict]:
    """Parse signed envelope and normalize payload to a structured event dict."""
    try:
        envelope = json.loads(raw_message)
    except json.JSONDecodeError:
        print(f"[WARN] Ignoring non-JSON message on topic={topic}")
        return None

    if not isinstance(envelope, dict):
        print(f"[WARN] Ignoring non-object envelope on topic={topic}")
        return None

    if not verify_envelope(envelope):
        print(f"[WARN] Invalid signature on topic={topic}")
        return None

    data = envelope["payload"]
    message_type = data.get("type")
    peer_id = data.get("peer_id")
    ts = data.get("ts")
    if not isinstance(message_type, str):
        print(f"[WARN] Missing/invalid type, peer_id, or ts on topic={topic}")
        return None

    if message_type == "TASK_CREATE":
        peer_id = peer_id if isinstance(peer_id, str) else "system"
        ts = ts if isinstance(ts, int) else int(time.time())
    elif not isinstance(peer_id, str) or not isinstance(ts, int):
        print(f"[WARN] Missing/invalid type, peer_id, or ts on topic={topic}")
        return None

    event = {
        "type": message_type,
        "peer_id": peer_id,
        "ts": float(ts),
        "role": data.get("role"),
        "task": data.get("task"),
        "task_id": data.get("task_id"),
        "result": data.get("result"),
    }
    return event


def append_proof_log(event_type: str, peer_id: str, ts: int, details: Optional[dict] = None) -> None:
    """Append-only audit trail for incoming events and state transitions."""
    details = details or {}
    event_body = {
        "type": event_type,
        "peer_id": peer_id,
        "ts": ts,
        "details": details,
    }
    event_id = sha256_hex(canonical_json(event_body))
    record = {
        "event_id": event_id,
        **event_body,
    }
    with PROOF_LOG_LOCK:
        PROOF_LOG.append(record)


def parse_task_spec(task_payload: dict) -> Optional[TaskSpec]:
    """Validate and normalize task schema."""
    if not isinstance(task_payload, dict):
        return None
    task_id = task_payload.get("task_id")
    task_type = task_payload.get("type")
    payload = task_payload.get("payload", {})
    requirements = task_payload.get("requirements", {})
    if not isinstance(task_id, str) or task_type not in {TASK_FAST, TASK_SECURE, TASK_RECOVERABLE}:
        return None
    if not isinstance(requirements, dict):
        return None
    try:
        req = TaskRequirements(
            min_agents=int(requirements.get("min_agents", 1)),
            required_role=str(requirements.get("required_role", "any")),
            max_latency_ms=int(requirements.get("max_latency_ms", 1000)),
            redundancy=int(requirements.get("redundancy", 1)),
        )
    except (TypeError, ValueError):
        return None
    if req.required_role not in {"worker", "leader", "any"}:
        return None
    if task_type == TASK_SECURE and req.redundancy < 2:
        return None
    if not isinstance(payload, dict):
        return None
    return TaskSpec(task_id=task_id, type=task_type, requirements=req, payload=payload)


def eligible_agents(state: Dict[str, PeerState], required_role: str) -> List[str]:
    peers = []
    for peer_id, peer in state.items():
        if peer.status != "ready":
            continue
        if required_role != "any" and peer.role != required_role:
            continue
        peers.append(peer_id)
    return sorted(peers)


def assign_task(task: TaskSpec, state: Dict[str, PeerState], previous_assignees: Optional[List[str]] = None) -> List[str]:
    """Deterministic assignment for FAST/SECURE/RECOVERABLE tasks."""
    candidates = eligible_agents(state, task.requirements.required_role)
    if len(candidates) < task.requirements.min_agents:
        return []

    if task.type == TASK_FAST:
        return candidates[:1]
    if task.type == TASK_SECURE:
        return candidates[: task.requirements.redundancy]
    if task.type == TASK_RECOVERABLE:
        if not previous_assignees:
            return candidates[:1]
        for candidate in candidates:
            if candidate not in previous_assignees:
                return [candidate]
        return candidates[:1]
    return []


def create_task_record(task: TaskSpec, state: Dict[str, PeerState]) -> dict:
    assignees = assign_task(task, state)
    lifecycle = TASK_ASSIGNED if assignees else TASK_CREATED
    return {
        "task_id": task.task_id,
        "type": task.type,
        "requirements": asdict(task.requirements),
        "payload": task.payload,
        "assignees": assignees,
        "state": lifecycle,
        "results": {},
    }


def handle_task_create(task_payload: dict, state: Dict[str, PeerState]) -> Optional[dict]:
    task = parse_task_spec(task_payload)
    if task is None:
        return None
    record = create_task_record(task, state)
    with TASKS_LOCK:
        TASKS[task.task_id] = record
    append_proof_log("TASK_CREATE", "system", int(time.time()), {"task_id": task.task_id, "assignees": record["assignees"]})
    return record


def handle_task_result(task_result: dict) -> bool:
    """Accept only assigned agent results; enforce SECURE_TASK matching outputs."""
    task_id = task_result.get("task_id")
    peer_id = task_result.get("peer_id")
    result = task_result.get("result")
    ts = task_result.get("ts")
    if not isinstance(task_id, str) or not isinstance(peer_id, str) or not isinstance(ts, int):
        return False
    with TASKS_LOCK:
        task = TASKS.get(task_id)
        if task is None or peer_id not in task["assignees"]:
            return False
        task["results"][peer_id] = result
        task["state"] = TASK_EXECUTING
        if task["type"] == TASK_SECURE:
            expected = len(task["assignees"])
            if len(task["results"]) >= expected:
                unique_results = {canonical_json({"result": value}) for value in task["results"].values()}
                if len(unique_results) == 1:
                    task["state"] = TASK_COMPLETED
                else:
                    task["state"] = TASK_ASSIGNED
                    task["results"] = {}
                    return False
        else:
            task["state"] = TASK_COMPLETED
    append_proof_log("TASK_RESULT", peer_id, ts, {"task_id": task_id})
    return True


def rebalance_recoverable_tasks(state: Dict[str, PeerState]) -> None:
    """Reassign recoverable tasks if current assignee becomes non-ready."""
    with TASKS_LOCK:
        for task in TASKS.values():
            if task["type"] != TASK_RECOVERABLE or task["state"] == TASK_COMPLETED:
                continue
            assignees = task.get("assignees", [])
            current = assignees[0] if assignees else None
            if current and state.get(current) and state[current].status == "ready":
                continue
            task_spec = TaskSpec(
                task_id=task["task_id"],
                type=task["type"],
                requirements=TaskRequirements(**task["requirements"]),
                payload=task["payload"],
            )
            new_assignees = assign_task(task_spec, state, previous_assignees=assignees)
            task["assignees"] = new_assignees
            task["state"] = TASK_ASSIGNED if new_assignees else TASK_CREATED
            task["results"] = {}


def to_millis(ts: int) -> int:
    """
    Normalize timestamps to epoch milliseconds.
    - 10-digit-ish values are interpreted as seconds
    - 13-digit-ish values are interpreted as milliseconds
    """
    return ts * 1000 if ts < 1_000_000_000_000 else ts


def seen_recently(event: dict) -> bool:
    """Replay protection cache based on canonical event hash."""
    event_hash = sha256_hex(canonical_json(event))
    if event_hash in RECENT_MESSAGE_HASHES_SET:
        return True
    if len(RECENT_MESSAGE_HASHES) == RECENT_HASH_CACHE_SIZE:
        evicted = RECENT_MESSAGE_HASHES.popleft()
        RECENT_MESSAGE_HASHES_SET.remove(evicted)
    RECENT_MESSAGE_HASHES.append(event_hash)
    RECENT_MESSAGE_HASHES_SET.add(event_hash)
    return False


def reduce_state(previous: Optional[PeerState], event: dict) -> Optional[PeerState]:
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

    incoming_last_seen_ms = to_millis(event["ts"])
    if incoming_last_seen_ms < baseline.last_seen_ms:
        # Deterministic drop rule for delayed/out-of-order messages.
        return None

    role = event.get("role") if isinstance(event.get("role"), str) else baseline.role

    return PeerState(
        peer_id=peer_id,
        last_seen_ms=incoming_last_seen_ms,
        role=role,
        status="ready",
    )


def heartbeat_loop(client: mqtt.Client, agent_id: str) -> None:
    """Background liveness publisher."""
    while True:
        heartbeat = {
            "type": "HEARTBEAT",
            "peer_id": agent_id,
            "ts": int(time.time()),
        }
        publish_json(client, TOPIC_SWARM, heartbeat)
        time.sleep(HEARTBEAT_INTERVAL_SEC)


def recompute_roles(state: Dict[str, PeerState]) -> None:
    """Deterministically assign roles from lexicographically sorted ready peers."""
    ready_peers = sorted(peer_id for peer_id, peer in state.items() if peer.status == "ready")
    leader_peer_id = ready_peers[0] if ready_peers else None
    for peer_id, peer in state.items():
        if peer.status != "ready":
            peer.role = "worker"
        elif peer_id == leader_peer_id:
            peer.role = "leader"
        else:
            peer.role = "worker"


def apply_stale_detection(state: Dict[str, PeerState], now_ms_value: int) -> bool:
    """Mark peers stale if last_seen exceeds threshold and return whether anything changed."""
    changed = False
    for peer in state.values():
        is_stale = now_ms_value - peer.last_seen_ms > STALE_THRESHOLD_MS
        target_status = "stale" if is_stale else "ready"
        if peer.status != target_status:
            peer.status = target_status
            changed = True
    recompute_roles(state)
    return changed


def stale_monitor_loop() -> None:
    """Background stale checker."""
    while True:
        with STATE_LOCK:
            changed = apply_stale_detection(STATE, now_ms())
            rebalance_recoverable_tasks(STATE)
            if changed:
                snapshot = {k: asdict(v) for k, v in sorted(STATE.items(), key=lambda item: item[0])}
                print(f"[STALE] {json.dumps(snapshot, sort_keys=True)}")
        time.sleep(STALE_CHECK_INTERVAL_SEC)


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
        heartbeat_thread = threading.Thread(
            target=heartbeat_loop,
            args=(client, userdata["agent_id"]),
            daemon=True,
        )
        heartbeat_thread.start()
        stale_thread = threading.Thread(target=stale_monitor_loop, daemon=True)
        stale_thread.start()

    else:
        print(f"[ERROR] Connection failed: {reason_code}")


def on_message(client: mqtt.Client, userdata, message: mqtt.MQTTMessage):
    """Called for every consensus-ordered message that arrives from FoxMQ."""
    topic = message.topic
    payload = message.payload.decode("utf-8")
    recv_order_index = next_recv_order_index()

    print(f"[RECV] idx={recv_order_index} topic={topic} payload={payload}")
    append_proof_log(
        event_type="INCOMING_RAW",
        peer_id="unknown",
        ts=int(time.time()),
        details={"topic": topic, "recv_idx": recv_order_index, "payload": payload},
    )

    event = parse_message(topic, payload)
    if event is None:
        append_proof_log(
            event_type="INCOMING_REJECTED",
            peer_id="unknown",
            ts=int(time.time()),
            details={"topic": topic, "recv_idx": recv_order_index},
        )
        return

    with STATE_LOCK:
        if seen_recently(event):
            print(f"[DROP] replay peer_id={event['peer_id']} ts={event['ts']}")
            append_proof_log(
                event_type="INCOMING_REPLAY_DROP",
                peer_id=event["peer_id"],
                ts=event["ts"],
                details={"topic": topic, "recv_idx": recv_order_index},
            )
            return
        if event["type"] == "TASK_CREATE":
            created = handle_task_create(event.get("task"), STATE)
            if created is None:
                append_proof_log(
                    event_type="TASK_CREATE_REJECTED",
                    peer_id=event["peer_id"],
                    ts=event["ts"],
                    details={"topic": topic, "recv_idx": recv_order_index},
                )
            snapshot = {k: asdict(v) for k, v in sorted(STATE.items(), key=lambda item: item[0])}
            print(f"[STATE] {json.dumps(snapshot, sort_keys=True)}")
            return
        if event["type"] == "TASK_RESULT":
            accepted = handle_task_result(
                {
                    "task_id": event.get("task_id"),
                    "peer_id": event["peer_id"],
                    "result": event.get("result"),
                    "ts": event["ts"],
                }
            )
            if not accepted:
                append_proof_log(
                    event_type="TASK_RESULT_REJECTED",
                    peer_id=event["peer_id"],
                    ts=event["ts"],
                    details={"task_id": event.get("task_id")},
                )
        prev = STATE.get(event["peer_id"])
        next_state = reduce_state(prev, event)
        if next_state is None:
            print(
                f"[DROP] peer_id={event['peer_id']} incoming_ts={event['ts']} "
                f"current_last_seen_ms={prev.last_seen_ms if prev else 0}"
            )
            append_proof_log(
                event_type="INCOMING_DELAYED_DROP",
                peer_id=event["peer_id"],
                ts=event["ts"],
                details={"topic": topic, "recv_idx": recv_order_index},
            )
            return
        previous_snapshot = asdict(prev) if prev else None
        STATE[event["peer_id"]] = next_state
        append_proof_log(
            event_type="STATE_TRANSITION",
            peer_id=event["peer_id"],
            ts=event["ts"],
            details={"previous": previous_snapshot, "next": asdict(next_state), "source_type": event["type"]},
        )
        apply_stale_detection(STATE, now_ms())
        rebalance_recoverable_tasks(STATE)
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
    """Publish a signed envelope with payload and signature (QoS 1)."""
    envelope = {
        "payload": data,
        "sig": sign_payload(data),
    }
    payload = json.dumps(envelope, sort_keys=True)
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
