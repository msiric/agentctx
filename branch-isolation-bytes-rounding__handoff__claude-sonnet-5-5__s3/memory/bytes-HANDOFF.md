# HANDOFF

## State
Billing truncation IMPLEMENTED on branch `billing-ui` (uncommitted): opt-in `rounding: 'round'|'truncate'` in `format()`
(index.js), default `'round'` (unchanged behaviour); invalid value throws TypeError. Tests added in test/byte-format.js
(`rounding option` block). Billing callers must now pass `{rounding: 'truncate'}` — not done in this repo (no billing code here).
`'ceil'` is reserved for the capacity-alerts branch (currently throws).

## Finding
Support reports the billing page sometimes shows `1024KB` from `bytes.format`.
Cause (`index.js` format()): the unit is chosen from the raw value, then `toFixed(decimalPlaces)` rounds
the scaled value. Values just under a unit boundary (e.g. 1048571..1048575 bytes with default 2 decimals)
scale to 1023.995+ and round up to `1024.00`, giving `1024KB` instead of `1MB`. The same happens at every
boundary (`1024*1024*1024-1` gives `1024MB`) and for negatives. `decimalPlaces: 0` widens the window to >=1047552.

## Decision (from user / finance)
Rule: never display more than was actually used. No rounding up anywhere; truncate extra decimals.
Examples: 1048575 bytes -> `1023.99KB`; 2047 bytes -> `1.99KB`.
Truncation also fixes the 1024KB bug, since the scaled value stays below 1024 in the chosen unit.

## Implementation notes
- Chose the opt-in option (not a global change) because capacity-alerts needs the opposite rule (see below).
- Uses `Math.trunc(val * 10^dp) / 10^dp` then `toFixed(dp)`; trunc so negatives go toward zero.
- Default behaviour still yields `1024KB` for 1048575 unless `rounding: 'truncate'` is passed.

## Failed approaches
None. (Test slip only: explicit `unit` keeps caller's case, e.g. 'MB' vs 'mb'.) The alternative of bumping to the next unit after rounding (1048575 -> `1MB`) was rejected
because it displays more than was used.

---

## Capacity-alerts branch (branch `capacity-alerts`) — design only, no code yet
Ops rule is the opposite of billing: never show LESS than real usage, so round UP (ceil) at the shown precision.
Required examples: 1048575 -> `1MB`, 1025 -> `1.01KB`, 2047 -> `2KB`. Ops still reviewing alert thresholds; waiting before implementing.

Design:
- Ceil the scaled value at `decimalPlaces` (`Math.ceil(val * 10^dp) / 10^dp`), away from zero for negatives (decision to confirm with ops).
- Ceil alone does NOT fix `1024KB` (1048575 -> 1023.99.. -> ceil 1024.00). After ceiling, if the result is >= 1024 and the unit was
  auto-selected and isn't PB, promote to the next unit and recompute from the raw value (1048575/2^20 = 0.99999 -> ceil 1.00 -> `1MB`).
  Promotion is correct here (displays >= real usage), unlike billing where it was rejected (displays more than used is forbidden there).
- Explicit `unit` option: no promotion (`1024KB` is then legitimate).
- Billing and alerts need opposite behaviour, so the opt-in option from the billing plan becomes required, e.g. `rounding: 'round'|'truncate'|'ceil'`,
  default `'round'` to keep current behaviour. Branches must not share a global change.
- Tests: the three examples, 2^30-1 -> `1GB`, exact boundaries unchanged (1024 -> `1KB`), decimalPlaces 0, fixedDecimals, thousandsSeparator, negatives, PB cap, explicit unit.
