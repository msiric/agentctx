# capacity-alerts

Branch: capacity-alerts · Repo: local__bytes-692788582 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: Ops (capacity-alerts) want bytes.format to round UP to shown precision, never under-report: 1048575 -> 1MB, 1025 -> 1.01KB, 2047 -> 2KB. Opposite of billing-ui (truncate). Must be opt-in, not a default change, since both rules hit the same format(). Design described only; no code yet, ops still reviewing alert thresholds.

