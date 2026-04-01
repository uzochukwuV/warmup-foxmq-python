# Stateful Swarm Agent — Current Stage Analysis (Code-Verified)

## Overall Stage

**Current stage: late prototype / pre-production hardening.**

From direct code inspection, the project already implements the full Issue 1–12 surface area in one process (`node.py`) plus deterministic/unit scenario tests (`test_node.py`). The highest remaining work is **robustness hardening and operational correctness**, not missing core feature scaffolding.

---

## Issue-by-Issue Assessment

### Issue 1 — Base connectivity & deterministic messaging
**Status:** Implemented.

- MQTT v5 client with credential login is in place.
- Subscriptions include both `swarm/state` and `swarm/hello`.
- HELLO payload publishes on connect.
- Receive order index and raw payload/topic logging exists.

### Issue 2 — Replicated state model
**Status:** Implemented.

- `PeerState` schema is present.
- Global `STATE` map with `STATE_LOCK` exists.
- Incoming events are parsed and reduced to deterministic state transitions.

### Issue 3 — Deterministic update engine
**Status:** Implemented.

- Update gate `incoming_last_seen_ms < baseline.last_seen_ms => drop` is enforced.
- Timestamp normalization (`to_millis`) handles second/ms inputs.
- Replay suppression cache exists.

### Issue 4 — Heartbeat protocol
**Status:** Implemented (functional, with reconnect caveat).

- 2s heartbeat background loop publishes to `swarm/state`.
- Accepted events refresh `last_seen_ms`.

### Issue 5 — Stale node detection
**Status:** Implemented (with determinism caveat).

- Threshold is configured at 5000ms.
- Periodic stale monitor marks peers `ready`/`stale`.

### Issue 6 — Deterministic role assignment
**Status:** Implemented.

- Ready peers sorted lexicographically.
- First peer is leader, others workers.
- Recomputed after updates/stale detection.

### Issue 7 — Message integrity
**Status:** Implemented with stronger-than-spec authentication.

- Envelope structure exists.
- Signature is **HMAC-SHA256** with shared secret (`SWARM_SIGNING_SECRET`), which is stronger than plain SHA256(payload).
- Invalid signatures are rejected before state mutation.

### Issue 8 — Replay protection
**Status:** Implemented.

- Old timestamps are rejected in reducer.
- Recent-message hash cache blocks immediate duplicates.

### Issue 9 — Proof log
**Status:** Implemented in memory.

- Append-only `PROOF_LOG` with event IDs and transition metadata.
- Includes rejected/drop events and state transitions.

### Issue 10 — Fault injection testing
**Status:** Implemented at deterministic test-harness level.

- Test suite covers replay, tamper, delayed messages, stale detection, and convergence across simulated peers.

### Issue 11 — Task coordination layer
**Status:** Implemented.

- Deterministic filtering/sorting/assignment for FAST, SECURE, RECOVERABLE tasks.
- Task lifecycle and SECURE result matching rules are present.
- Recoverable reassignment logic is present.

### Issue 12 — End-to-end scenario
**Status:** Implemented as in-process deterministic scenario.

- `run_end_to_end_scenario` exercises all task types and recoverable reassignment.
- Tests verify deterministic snapshots across repeated runs.

---

## Bugs to Fix at This Stage (Priority Ordered)

### P0 — Reconnect can spawn duplicate background loops
`on_connect` always starts new heartbeat and stale-monitor threads. If the MQTT client reconnects, additional loops are created, causing duplicate heartbeats and redundant stale checks.

**Fix:** Add idempotent thread-start guards (e.g., flags/events in userdata or module-level singleton thread handles).

### P0 — Event timestamp type drift (`float` vs `int`)
`parse_message` emits `event["ts"]` as `float` while several downstream paths expect `int` semantics (task result validation, logging consistency).

**Fix:** Keep `ts` strictly `int` end-to-end, normalize once at parse boundary.

### P1 — Determinism leak from local wall-clock stale checks
`apply_stale_detection` is called using each node’s local clock (`now_ms()`), so peers with clock skew can temporarily disagree on stale classification.

**Fix options:**
- Base stale evaluation on consensus-ordered time beacons/messages, or
- require monotonic logical time derived from message stream for deterministic classification windows.

### P1 — Lock contention / lock scope risk
`on_message` takes `STATE_LOCK` and may call task handlers that also use `TASKS_LOCK`; stale monitor also uses both paths. Current order appears consistent, but nested locking scope is broad.

**Fix:** Standardize lock ordering + reduce critical sections to avoid deadlock regressions as complexity grows.

### P2 — Proof log and tasks are volatile
`PROOF_LOG` and `TASKS` are in-memory only; restart loses audit trail and in-flight task context.

**Fix:** Optional write-ahead append log and periodic snapshots.

---

## Optimizations Appropriate for the Current Stage

1. **Thread lifecycle hardening**
   - Single heartbeat/stale loop per process.
   - Stop events for clean shutdown/tests.

2. **Strict schema contracts**
   - Enforce typed dataclasses/pydantic-style validation for inbound events.
   - Explicit enum validation for message types and statuses.

3. **Determinism observability**
   - Include stable event hash + recv index in every proof record.
   - Add deterministic snapshot checksum endpoint/log line.

4. **Replay cache durability and scale**
   - Move from bounded hash set to time-windowed structure keyed by peer+ts(+nonce).
   - Optionally persist recent window across restart.

5. **Higher-fidelity multi-process tests**
   - Current tests are excellent deterministic unit/system simulations; add real multi-process integration against FoxMQ to validate reconnect/thread behavior.

---

## Recommended Next Milestone

**Milestone: “Production Determinism Hardening”**

- Fix reconnect-thread duplication.
- Enforce integer timestamp contract.
- Make stale classification deterministic under clock skew assumptions.
- Add persistence for proof log/task state.
- Add 3-agent+ live integration test in CI.

This would move the project from “feature-complete prototype” to “operationally reliable coordinator runtime.”
