# HANDOFF

## State
DONE on billing-ui (uncommitted): `format()` in `index.js` now truncates toward zero instead of rounding, via new helper `truncate()`. Tests added/updated in `test/byte-format.js`; 33 passing, eslint clean. User said we're cleared to make the fix.
- Whole-byte inputs: exact expansion (`toFixed(100)`; /2^k is exact in binary) then slice, so 1048575 -> `1023.99KB`.
- Fractional inputs: `toFixed(decimalPlaces+12)` then slice, because `1.2*kb/kb` is 1.19999999999999996 and exact truncation would show `1.19KB`. Tests cover 1.1/1.2/1.15 KB, 4.35MB.
- `-0.001` -> `0B` (no `-0`).
- Updated existing tests that expected rounding (1.5KB dp0 -> `1kb`; 1.05KB dp1 -> `1kb`).
- STILL OPEN: this changes the default for ALL callers of `bytes.format` (I applied it globally, following the "no rounding up anywhere" decision). If it should be billing-only, make it an option instead. Finance wording sign-off also still pending. Not committed.

## Findings
- Billing page showing `1024KB` comes from `format()` in `index.js`. The unit is chosen from the raw value, then `val.toFixed(decimalPlaces)` rounds. A value just under a unit boundary stays in the smaller unit and rounds up to 1024 (e.g. `format(1048575)` -> `1024KB`, `1073741823` -> `1024MB`, `-1048575` -> `-1024KB`).
- Window is the last ~0.005 of a unit with default `decimalPlaces: 2`; wider with lower `decimalPlaces` (0 -> anything >= 1023.5 KB).
- Forced `unit` option does not trigger it.

## Decision (from user, finance rule)
Billing must never display more than was actually used: no rounding up anywhere, truncate extra decimals instead.
- 1048575 bytes -> `1023.99KB` (not `1024KB`, not `1MB`)
- 2047 bytes -> `1.99KB`

Reason: finance policy. This rules out the earlier idea of "round, then bump to next unit" since that would show 1MB for 1048575.

## Planned change (not done)
In `format`, replace `toFixed(decimalPlaces)` rounding with truncation toward zero at `decimalPlaces` digits (watch float error, e.g. use integer math / string slicing on a high-precision toFixed rather than Math.floor(val*10^n)). Keep unit selection on the raw value, which is then correct. Check negatives (truncate toward zero), `fixedDecimals`, `thousandsSeparator`, and update existing tests that expect rounding.

## Open questions
- Finance sign-off on page wording.
- Whether truncation should apply to all callers of `bytes.format` or only billing (e.g. a new option); this changes the library's default behavior for everyone otherwise.

## capacity-alerts branch (design only, no code changed)
Ops want the opposite of billing: never show less than real usage, so round UP (ceiling) at the shown precision.
- 1048575 -> `1MB`, 1025 -> `1.01KB`, 2047 -> `2KB`.
- Design: keep unit choice on raw value; ceil magnitude at `decimalPlaces` (away from zero for negatives); if result reaches 1024 and unit not forced and not PB, bump to next unit as 1. Forced `unit` stays e.g. `1024KB`.
- Use integer math / high-precision string for the ceiling; `Math.ceil(val*100)/100` overshoots (1.1*100 = 110.00000000000001).
- Reason for an option (e.g. `rounding: 'ceil'`) rather than a new default: billing wants truncation, other callers expect nearest rounding.
- `decimalPlaces: 0` makes 1025 bytes -> `2KB`; ops to confirm acceptable.
- Waiting on ops to finish reviewing alert thresholds before any edit.
