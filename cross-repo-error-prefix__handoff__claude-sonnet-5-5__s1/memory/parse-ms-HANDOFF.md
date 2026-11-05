# Handoff

## State
`largestUnit` option ('days' default | 'hours' | 'minutes' | 'seconds') added to `parseMilliseconds` (index.js, index.d.ts, readme, tests). `npm test` passes (xo, node --test, nz).

## Decisions
- Units above the largest are `0` (keys stay present). Largest unit is the plain quotient; smaller ones stay remainder-based, keeping the earlier exactness at any magnitude.
- Invalid value (incl. null) throws TypeError, validated before the input, for number and bigint alike.
- Negative numbers keep existing `-0` behaviour for micro/nanoseconds; tests expect it.

## Failed approaches
- Type tests with a literal argument infer `T` as `3000`; annotate the result variable instead.
