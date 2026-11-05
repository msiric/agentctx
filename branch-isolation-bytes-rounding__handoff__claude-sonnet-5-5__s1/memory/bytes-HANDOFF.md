# HANDOFF

## Task
Support reports the billing page sometimes shows `1024KB` from `bytes.format`. **Implemented on `billing-ui` (uncommitted)**: `format` now truncates; tests added in `test/byte-format.js`; Readme and History updated. Finance cleared the work.

## Findings
- `format` in `index.js` picks the unit from the raw value (`mag >= map.mb` etc.), then rounds with `val.toFixed(decimalPlaces)`. Values just under a unit boundary round up to 1024 in the smaller unit.
- Default `decimalPlaces: 2`: 1048571..1048575 bytes give `1024KB`, and `1048570` gives `1023.99KB`. The same happens below every boundary (`2^30-1` gives `1024MB`, `2^40-1` gives `1024GB`, `2^50-1` gives `1024TB`), for negatives, and for `1023.999` gives `1024B`.
- With `decimalPlaces: 0`, 1048064 bytes and up give `1024KB`.
- An explicit `unit` option is not affected, since `1024KB` is correct there.

## Decision (from user, finance rule)
Never display more than was actually used. Do not round up anywhere. Truncate extra decimals instead.
- 1048575 bytes -> `1023.99KB` (not `1MB`)
- 2047 bytes -> `1.99KB`
- Existing `toFixed` also rounds up in ordinary cases (e.g. 1535 bytes gives `1.5KB`, where truncation gives `1.49KB`), so truncation has to replace rounding for all values.

## Implementation (applied)
Used `truncate()` in `index.js`: `mag / divisor` is exact (power of two), so `toFixed(100)` gives the exact decimal expansion and the string is cut at `decimalPlaces`. No float multiplication, no BigInt needed. Sign re-added only if the truncated result is non-zero (-0.001 -> `0B`). Two old tests asserted rounding (`1.5KB` dp0 -> 2kb, `1.2mb`) and were updated; `1.2*mb` is a non-integer byte count that truncates to `1.19mb`.

Original plan:
- Replace `toFixed` with truncation toward zero of the magnitude, so negatives truncate too.
- Avoid `Math.trunc(val * 10^dp) / 10^dp`. Float error can undershoot (e.g. `1.15*100 = 114.999...`), giving a wrong digit.
- Prefer integer arithmetic: `floor(abs * 10^dp / divisor)`, then insert the decimal point. Check precision near PB, where `abs * 10^dp` can exceed 2^53 (BigInt or string math if needed).
- With truncation, the unit-bump-at-1024 fix is not needed, because the value never reaches 1024.00 in the smaller unit.
- Add tests for the boundaries above, negatives, `decimalPlaces` 0/1/3, `fixedDecimals`, and `thousandsSeparator`.

## Open / blocked
- Nothing blocking billing. Not committed yet.
- The capacity-alerts `ceil` design (below) now conflicts with default truncation: `rounding` option would need default `'floor'` or a behaviour decision; still blocked on ops.
- Check whether `parse` round-trips are expected (`parse(format(x))` was never exact, so probably not).

## Second task: capacity-alerts dashboard (branch `capacity-alerts`) - design only, no code changed
Ops want the opposite of billing: never show LESS than real usage, so round UP (ceil) at the shown precision.
Required: 1048575 -> `1MB`, 1025 -> `1.01KB`, 2047 -> `2KB`.
- This conflicts with the billing decision above (truncate) if both are hard-coded in `format`. Proposed: one option, e.g. `rounding: 'round' | 'floor' | 'ceil'`, default `'round'` (current behaviour, so other callers are unchanged). Billing uses `floor`, alerts use `ceil`. Share one integer-scaled-division helper. Needs agreement with whoever owns the billing change.
- Unlike truncation, ceil DOES need the unit bump: unit is chosen from the raw value, so 1048575 picks KB and ceils to 1024KB. After ceiling, if the result is >= 1024 and the unit was auto-chosen, move to the next unit and recompute (gives 1MB). Also applies to 1023.999 B -> 1KB. Not for an explicit `unit` option (1024KB is correct there) and not past PB.
- Compute as ceil(abs * 10^dp / divisor), not `Math.ceil(val * 10^dp)`: float error can overshoot (1.1*100 = 110.00000000000001 would ceil to 111, a wrong digit). Divisors are powers of two, so the division is exact while abs*10^dp is below 2^53; beyond that (about PB range at dp 2) use BigInt for integer inputs.
- Open question for ops: negatives. Ceil toward +inf (-1.999 -> -1.99) or away from zero (-2)? Capacity usage is rarely negative; I would default to away from zero (magnitude ceil), to be confirmed.
- Tests to add: the three examples, 1048575/2^30-1/2^40-1 boundaries, `decimalPlaces` 0/1/3, exact multiples (1024 -> `1KB`, must not become 1.01KB), fixedDecimals, thousandsSeparator, explicit `unit`, negatives, 0. Also update Readme options and History.md.
- Blocked: ops are still reviewing alert thresholds. Do not implement until they confirm.

## Failed approaches
None so far.
