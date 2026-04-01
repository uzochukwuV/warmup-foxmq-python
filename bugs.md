# Bug Fix Log — Production Determinism Hardening

This file documents the bug fixes requested from the prior issue-stage review and how they were implemented.

## P0 — Reconnect spawning duplicate background loops

### Problem
`on_connect` started heartbeat/stale monitor threads every time reconnect fired, which could create duplicate loops over long-lived runs.

### Fix
- Added module-level singleton thread guards:
  - `HEARTBEAT_THREAD`
  - `STALE_THREAD`
- `on_connect` now starts each loop only if the existing thread is missing or not alive.

### Outcome
Only one heartbeat loop and one stale monitor loop run per process lifecycle.

---

## P0 — Timestamp type drift (`float` vs `int`)

### Problem
`parse_message` emitted `event["ts"]` as `float`, while task and state logic rely on integer semantics.

### Fix
- `parse_message` now normalizes `ts` to `int` at parse time.
- Internal processing paths continue using integer timestamps end-to-end.

### Outcome
Consistent timestamp typing across validation, state reduction, and task-result handling.

---

## P1 — Determinism leak from wall-clock stale checks

### Problem
Stale detection used local `now_ms()`, allowing clock skew to temporarily diverge stale/ready classification between peers.

### Fix
- Added consensus-derived logical clock helpers:
  - `advance_logical_time(ts)`
  - `get_logical_time_ms()`
- `on_message` advances logical time from accepted event timestamps.
- Stale checks now use logical time (`get_logical_time_ms()`) rather than local wall time.

### Outcome
Stale classification is now derived from message stream time progression, reducing cross-node skew divergence.

---

## P1 — Lock contention / broad nested lock scope

### Problem
Message handling combined `STATE_LOCK` and `TASKS_LOCK` through nested call paths, increasing deadlock/regression risk as complexity grows.

### Fix
- Reduced lock scope in `on_message`:
  - Task operations are handled outside `STATE_LOCK`.
  - State updates are done in short, focused `STATE_LOCK` blocks.
- Recoverable rebalancing is invoked using snapshots rather than in deeply nested lock chains.

### Outcome
Lower lock coupling and clearer lock boundaries for future extension.

---

## P2 — Volatile in-memory proof/task state

### Problem
`PROOF_LOG` and `TASKS` only lived in process memory; restart dropped audit history and in-flight coordination context.

### Fix
- Added optional persistence hooks controlled by env vars:
  - `SWARM_PROOF_LOG_PATH` for append-only JSONL proof records
  - `SWARM_TASKS_SNAPSHOT_PATH` for JSON task snapshots
- `append_proof_log` and task mutation paths now persist when configured.

### Outcome
Operators can enable lightweight write-ahead/snapshot durability without changing runtime behavior when unset.
