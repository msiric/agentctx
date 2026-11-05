# Handoff

## State
`largestUnit` option ('days' default | 'hours' | 'minutes' | 'seconds') added to `parseMilliseconds` (index.js, index.d.ts, readme, tests in test.js / index.test-d.ts). Works for number and bigint; any other value throws TypeError. `xo` and `node --test` pass.

## Decisions
- The largest unit is computed as `trunc(ms / unit)` over the whole value; units above it are set to 0 (positive zero, even for negative input, unlike the default path's `-0` for days).
- Validation runs before the input type check, so a bad option throws for any input.
- Sub-second parts are unchanged.

## Failed/notes
- First test draft expected `days: -0` for negative input; rolled units are plain `0`, so the test was corrected.
