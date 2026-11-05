# main

Branch: main · Repo: local__pretty-bytes-1046133736 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: unit option (commit 6033815): my choice, not the user's: a forced unit skips the unit-boundary correction/carry, so 999999 with unit kB prints '1000 kB'. Types are a flat union of all unit names and are not narrowed by bits/binary; the runtime TypeError is the only mismatch check.
- 2026-11-05: significantDigits (my choice): valid = integer 1..100, anything else silently falls back to 3 (per repo rule: new options never throw). Applies via the existing toPrecision path, so integer digits are never cut (999 with significantDigits:1 stays '999 B'). Ignored when either fraction-digit option is set.

