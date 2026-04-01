# Stateful Swarm Agent — Current Stage Analysis

## Executive summary

The current codebase has completed most of Issues **1–8** at a functional baseline level, but lacks Issues **9–12** (proof-log, fault-injection suite, task coordination layer, and end-to-end scenario orchestration).

Current maturity is best described as:

- **Stage:** Core swarm replication runtime (pre-coordination)
- **Readiness:** solid prototype for deterministic state sync, liveness, and basic security validation
- **Main gap:** no deterministic task scheduler/executor layer yet

---

## Issue-by-issue status

### ISSUE 1 — Base Connectivity & Deterministic Messaging
**Status:** ✅ Mostly implemented

Implemented:
- MQTT v5 client + credentials + connect lifecycle
- Subscribe to `swarm/state` and `swarm/hello`
- Publish HELLO with `{type, peer_id, ts}`
- Receive logging includes topic, payload, receive index

Risk / gap:
- "No duplicate or missing messages" is only partially addressed at app layer (replay cache), but no explicit delivery audit counters per topic/peer.

### ISSUE 2 — Replicated State Model
**Status:** ✅ Implemented

Implemented:
- `PeerState` dataclass with required schema fields
- `STATE` + `STATE_LOCK`
- Message parsing to structured event
- Deterministic state transition function (`reduce_state`)

### ISSUE 3 — Deterministic Update Engine
**Status:** ✅ Implemented

Implemented:
- Rule: apply update only when incoming timestamp is >= current
- Out-of-order drop behavior
- Input normalization (`to_millis`) for seconds/ms
- Deterministic handling of duplicates via replay cache

### ISSUE 4 — Heartbeat Protocol
**Status:** ✅ Implemented

Implemented:
- Background heartbeat thread every 2 seconds
- HEARTBEAT publish to `swarm/state`
- `last_seen_ms` updated on any accepted signed event (`HELLO` or `HEARTBEAT`) because reduce/apply path is type-agnostic

### ISSUE 5 — Stale Node Detection
**Status:** ✅ Implemented

Implemented:
- Runtime uses `STALE_THRESHOLD_MS = 5000` (5 seconds)
- periodic stale checker thread
- status transitions `ready ↔ stale`

Risk / gap:
- stale detection uses local wall clock and is not event-sourced; in extreme clock skew, classifications can differ across nodes.
- Documentation mismatch: README challenge text still describes stale after >10 seconds, so observed runtime behavior can differ from README expectations.

### ISSUE 6 — Deterministic Role Assignment
**Status:** ✅ Implemented

Implemented:
- Lexicographic ready-peer sort
- First ready peer is `leader`, others `worker`
- Recomputed after stale detection / state updates

### ISSUE 7 — Message Integrity
**Status:** ✅ Implemented

Implemented:
- Envelope with payload + HMAC-SHA256 signature (shared secret)
- Signature verification before processing
- Invalid signatures rejected

Gap:
- Uses a shared secret model (symmetric authentication); no asymmetric identity yet.

### ISSUE 8 — Replay Protection
**Status:** ✅ Implemented (baseline)

Implemented:
- Reject old timestamps (`incoming.ts < current.last_seen_ms`)
- Recent hash cache for duplicate suppression

Gap:
- Hash cache is process-local and bounded; long-window replays can bypass cache if timestamp still acceptable.

### ISSUE 9 — Proof Log (Auditability)
**Status:** ✅ Implemented

Implemented:
- append-only in-memory proof log list
- incoming message audit records (`INCOMING_RAW` + rejection/drop outcomes)
- state transition records with before/after snapshots

Gap:
- no persistence/export yet (log is process-memory only)

### ISSUE 10 — Fault Injection Testing
**Status:** ✅ Implemented (deterministic test harness)

Implemented:
- unit tests cover parsing, tamper rejection, timestamp ordering, replay cache, stale detection, role assignment
- 50-agent fault-injection stream test for replay, delayed messages, stale detection, and deterministic snapshot convergence

### ISSUE 11 — Task Coordination Layer
**Status:** ✅ Implemented (core deterministic scheduler)

Implemented:
- strict task schema parser (`TaskSpec` + `TaskRequirements`)
- deterministic eligibility filter (`ready` + role)
- deterministic assignment rules for FAST/SECURE/RECOVERABLE
- lifecycle states (`CREATED → ASSIGNED → EXECUTING → COMPLETED`)
- SECURE result-matching enforcement
- RECOVERABLE reassignment on stale assignee

### ISSUE 12 — End-to-End Scenario
**Status:** ✅ Implemented (50-agent deterministic scenario harness)

Implemented:
- scripted E2E scenario with 50 agents and deterministic role/bootstrap state
- FAST/SECURE/RECOVERABLE task injection and completion assertions
- recoverable-agent kill/stale simulation with automatic reassignment
- cross-run consistency checks for task snapshots and proof logs

---

## Priority bugs to fix now (current stage)

1. **Potential nondeterminism source (Issue 5):** stale classification depends on local wall clock, not consensus events.
2. **Reconnect/thread lifecycle bug risk:** `on_connect` starts heartbeat/stale threads each reconnect; repeated reconnects can create duplicate background loops.
3. **Timestamp unit ambiguity:** code accepts seconds or ms; mixed publishers may cause coarse-order edge effects.
4. **Replay cache memory/logic edge:** bounded cache can miss repeated old duplicates over long runtimes.
5. **Task persistence gap:** in-memory task/proof records are not persisted across process restarts.

---

## Stage-appropriate optimizations

1. **Thread idempotency guard**
   - Ensure heartbeat/stale threads are started once per process.

2. **Deterministic monotonic event sequencing metadata**
   - Include broker-sequence/receive index in append-only log for offline checks.

3. **Stricter schema validation**
   - Enforce allowed `type` enum and role/status enums.

4. **Stable serialization helpers**
   - Use canonical serializer centrally for all outbound/inbound comparisons.

5. **Testing upgrades before Issue 11**
   - Add integration tests with 3 agents and deterministic expected snapshots.

---

## Recommended roadmap

1. Finish **Issue 9** first (proof logging), because it will make all later debugging measurable.
2. Expand **Issue 10** with multi-process fault injection tests.
3. Implement **Issue 11** task coordination primitives in pure deterministic reducers.
4. Build **Issue 12** scenario harness and CI gate.
