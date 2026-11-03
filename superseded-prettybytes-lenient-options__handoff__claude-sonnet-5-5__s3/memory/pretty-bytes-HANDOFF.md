# Handoff

## State
`unit` option implemented and finished (index.js, index.d.ts, readme.md, test.js, index.test-d.ts). `npm test` (xo, ava, tsd) passes.

## Decisions
- `unit` is validated against the unit list chosen by `bits`/`binary`; anything else (wrong system, wrong case, non-string) throws TypeError.
- A forced unit skips the "just below a boundary" exponent correction and the round-up-to-next-unit bump, so the unit is never changed after being forced (e.g. 999999 bytes with `kB` gives `1000 kB`).
- Typed as `string` rather than a union of unit literals.

## Failed approaches
None.

## Policy (from user, applies to future work)
New options must never throw on a bad value: ignore it and format as if the option was not passed (a stale saved pref crashed the storage dashboard after the `unit` release). `unit` already shipped with its TypeError, so it stays as is until the next major.

## significantDigits
Added `significantDigits` (index.js, index.d.ts, readme.md, test.js, index.test-d.ts). Valid: integer 1-100 (the `toPrecision` range). Per the policy above, invalid values are ignored and fall back to 3, never throw. It is the floor in `Math.max(sig, integer digits)`, so the integer part is never cut short. Ignored whenever a fraction-digit option is set.

## Previous change
Added a `{bits: true, unit: 'Mbit'}` example to the readme `unit` section and a matching test.
