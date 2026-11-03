# HANDOFF

## State
Added `compound` option to `format`/`ms` (src/index.ts, `fmtCompound`) + tests in src/format.test.ts. Committed on feat/compound-format. Tests cover mixed units, ms truncation, negatives, ms() entry point, long precedence, boundaries.

## Decisions
- Units: d/h/m/s only; leftover ms floored (truncated), per request.
- Values under 1s (incl. negative) give `0s` (no `-0s`) since no parts remain.
- `compound` takes precedence over `long`; output is always short names.
- README documents compound ("Compound Format" section) with the current space-separated d/h/m/s output.

## Update: parse whitespace (done)
- `parse()` now matches against `str.trim()`; length check still applies to the raw string. Whitespace-only -> NaN. Tests in src/parse.test.ts.

## Pending: compound format change (NOT done yet, user deferred)
- Compound output must be Go `time.ParseDuration` compatible: no spaces, hours as largest unit, e.g. `25h30m` instead of `1d 1h 30m`. Needs changes to `fmtCompound`, its tests, and the decisions above (d unit dropped).

## Update: README + extra tests (done)
- Added README section and tests (compound:false, fractional ms, large day counts, invalid input). Node tests, lint, typecheck, format pass.
- If the Go-compatible change above is made, the README examples (`1h 30m`, `1d 1h 1m 1s`) and these tests must be updated too.
