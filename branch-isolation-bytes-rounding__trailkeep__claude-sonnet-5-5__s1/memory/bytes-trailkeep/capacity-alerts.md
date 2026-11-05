# capacity-alerts

Branch: capacity-alerts · Repo: local__bytes-598552995 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: capacity-alerts: ops want round UP (never show less than real usage): 1048575->1MB, 1025->1.01KB, 2047->2KB. Opposite of billing (truncate, finance note). Same bytes.format, so must be an opt-in option, not a new default. Plan only; no code until ops finish reviewing alert thresholds.

