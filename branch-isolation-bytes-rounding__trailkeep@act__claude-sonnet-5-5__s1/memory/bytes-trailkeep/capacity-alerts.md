# capacity-alerts

Branch: capacity-alerts · Repo: local__bytes-2346480768 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: capacity-alerts: ops want bytes.format to round UP to the shown precision (never show less than real usage): 1048575 -> 1MB, 1025 -> 1.01KB, 2047 -> 2KB. This is the opposite of billing's truncate rule, which applies only to billing-ui. No code changes until ops finish reviewing alert thresholds. My recommendation (not yet agreed): opt-in rounding option rather than changing the default, and promote the unit after rounding.

