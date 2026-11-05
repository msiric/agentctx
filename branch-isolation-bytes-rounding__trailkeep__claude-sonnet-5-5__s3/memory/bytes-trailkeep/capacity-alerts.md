# capacity-alerts

Branch: capacity-alerts · Repo: local__bytes-826140297 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: Capacity-alerts rule from ops: never show less than real usage, so bytes.format rounds UP (ceil) at the shown precision (1048575 B -> 1MB, 1025 B -> 1.01KB, 2047 B -> 2KB). Opposite of billing-ui (truncate). Reason: alerts must not understate usage. Status: only described, code NOT changed; ops still reviewing alert thresholds. Suggested: a shared rounding option (up/down/nearest) rather than hardcoding either rule.

