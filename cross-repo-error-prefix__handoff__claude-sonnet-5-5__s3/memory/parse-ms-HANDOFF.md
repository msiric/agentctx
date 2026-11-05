# Handoff

## State
`largestUnit` option ('days' default, 'hours', 'minutes', 'seconds') added to `parseMilliseconds` (index.js, index.d.ts, readme, tests). Works for number and bigint; any other value throws TypeError (the option is validated before the input).

## Decisions
- Rolled-up unit = `(ms - ms % size) / size` rather than `trunc(ms / size)`: a large quotient can round up to the next integer; the remainder form is exact.
- Units above largestUnit are 0 (-0 for negative input, matching existing default behaviour for zero parts).

## Notes
- `npx tsd` fails on an unrelated `nz` module resolution error (pre-existing; not investigated).
