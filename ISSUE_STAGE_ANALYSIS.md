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
- `last_seen_ms` updated on accepted heartbeat events

### ISSUE 5 — Stale Node Detection
**Status:** ✅ Implemented

Implemented:
- `STALE_THRESHOLD_MS = 5000`
- periodic stale checker thread
- status transitions `ready ↔ stale`

Risk / gap:
- stale detection uses local wall clock and is not event-sourced; in extreme clock skew, classifications can differ across nodes.

### ISSUE 6 — Deterministic Role Assignment
**Status:** ✅ Implemented

Implemented:
- Lexicographic ready-peer sort
- First ready peer is `leader`, others `worker`
- Recomputed after stale detection / state updates

### ISSUE 7 — Message Integrity
**Status:** ⚠️ Partially implemented

Implemented:
- Envelope with payload + SHA256 signature
- Signature verification before processing
- Invalid signatures rejected

Gap:
- Current scheme is an integrity checksum, **not authentication** (no shared secret/keyed MAC or asymmetric signature). Any party can recompute SHA256 over tampered payload.

### ISSUE 8 — Replay Protection
**Status:** ✅ Implemented (baseline)

Implemented:
- Reject old timestamps (`incoming.ts < current.last_seen_ms`)
- Recent hash cache for duplicate suppression

Gap:
- Hash cache is process-local and bounded; long-window replays can bypass cache if timestamp still acceptable.

### ISSUE 9 — Proof Log (Auditability)
**Status:** ❌ Not implemented

Missing:
- append-only structured event log
- state-transition log records
- deterministic replay/reconstruction tooling

### ISSUE 10 — Fault Injection Testing
**Status:** ⚠️ Partially implemented

Implemented:
- unit tests cover parsing, tamper rejection, timestamp ordering, replay cache, stale detection, role assignment

Missing:
- process kill tests
- delayed network delivery simulation
- multi-agent divergence tests
- scenario tests for replay storms

### ISSUE 11 — Task Coordination Layer
**Status:** ❌ Not implemented

Missing:
- task schema models
- eligibility filter
- deterministic assignment (FAST/SECURE/RECOVERABLE)
- task lifecycle + result verification
- reassignment logic for stale assignees

### ISSUE 12 — End-to-End Scenario
**Status:** ❌ Not implemented

Missing:
- integrated test harness with 3+ agents
- scripted scenario flow and success assertions

---

## Priority bugs to fix now (current stage)

1. **Security semantics bug (Issue 7):** SHA256(payload) is not authenticating sender identity.
2. **Potential nondeterminism source (Issue 5):** stale classification depends on local wall clock, not consensus events.
3. **Reconnect/thread lifecycle bug risk:** `on_connect` starts heartbeat/stale threads each reconnect; repeated reconnects can create duplicate background loops.
4. **Timestamp unit ambiguity:** code accepts seconds or ms; mixed publishers may cause coarse-order edge effects.
5. **Replay cache memory/logic edge:** bounded cache can miss repeated old duplicates over long runtimes.

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

