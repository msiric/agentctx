# Handoff

## State
`unit` option implemented in index.js, with types (index.d.ts, index.test-d.ts), readme and tests (test.js). All tests pass.

## Decisions
- The unit is validated against the active system (`bits`/`binary`) via `assertUnit`; any other value throws TypeError. Matching is case-sensitive (`mb` throws).
- A forced unit sets the exponent directly. The auto-selection fix-ups (the below-boundary correction and the round-up-to-next-unit bump) are skipped, because they would change the unit.
- `bits` only changes the labels, so a forced bit unit scales the same way as the byte one.

## Notes
- xo warns that `prettyBytes` complexity is 22 (max 20). It is only a warning. Extracting the exponent choice into a helper would clear it.

## significantDigits
- Implemented in index.js (replaces the hard-coded 3 in `minimumPrecision`), types, readme, tests.
- Per the policy below, an invalid value (non-integer, <1, >100, non-number) is ignored and 3 is used; it never throws. Range 1-100 matches `toPrecision`.
- Only applies on the non-fraction-digit path, so fraction options win.

## Policy (from the user)
- New options must never throw on a bad value: ignore it and format as if the option was not passed (a stale saved preference such as `unit: 'KB'` crashed the dashboard's file table).
- `unit` already shipped with the throw, so leave it until the next major.

## Log
- Added a bits example (`{bits: true, unit: 'Mbit'}`) to the readme `unit` section and a matching test.
