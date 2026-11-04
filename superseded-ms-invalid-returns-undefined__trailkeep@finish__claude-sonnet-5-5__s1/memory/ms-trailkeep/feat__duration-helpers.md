# feat/duration-helpers

Branch: feat/duration-helpers · Repo: local__ms-1225694183 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: parseCompound accepts one optional comma between pieces only (lookahead requires another piece); leading/trailing/double commas throw TypeError. Shipped in 4.1.0-canary.1, so keep prior accepted inputs working.
- 2026-11-04: parseClock (m:ss / h:mm:ss) returns number|undefined, never throws/NaN per repo rule. Seconds and minutes-with-hours must be 2 digits <60; leading hours/minutes unbounded; no negatives, fractions, or whitespace (my choice, not user-specified).

