# billing-ui

Branch: billing-ui · Repo: local__bytes-692788582 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: Open for next session (billing-ui): (1) billing-only option like {rounding:'down'} vs changing default format behavior - undecided; (2) negatives: proposed truncating magnitude toward zero, not confirmed; (3) truncate via integer/string math, not Math.floor(val*10^n)/10^n, to avoid float error (1.15 -> 1.14); (4) add tests for boundaries 1048575 and 2047 and each unit boundary. Blocked on finance sign-off of page wording.
- 2026-11-05: Implemented opt-in {rounding:'down'} in format() (truncate via toFixed(100) string slice, negatives truncate magnitude, no '-0'); default still rounds (tests assert 1.5KB dp0 -> 2KB). Chosen because changing default would break existing public behavior; billing page must pass rounding:'down'. Flip default only if user decides.
- 2026-11-05: truncate() uses String(mag) (shortest repr) not exact expansion: exact expansion of double 1.15 is 1.1499.. -> would give 1.14; shortest repr gives intended 1.15.

