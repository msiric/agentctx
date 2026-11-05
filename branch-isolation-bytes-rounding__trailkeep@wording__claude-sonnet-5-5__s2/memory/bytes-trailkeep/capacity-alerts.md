# capacity-alerts

Branch: capacity-alerts · Repo: local__bytes-4046641431 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: capacity-alerts: ops want bytes.format to round UP (never show less than real usage) at the shown precision: 1048575->1MB, 1025->1.01KB, 2047->2KB. This is the opposite of billing-ui's truncate rule (finance), so it must NOT change the default behaviour; plan is an opt-in option. User said describe only, no code changes yet (ops still reviewing alert thresholds). My choices, not user's: option name, ceil on magnitude for negatives, integer-based math.

