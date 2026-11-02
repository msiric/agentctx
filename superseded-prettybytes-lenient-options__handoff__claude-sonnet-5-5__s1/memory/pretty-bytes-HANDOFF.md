# HANDOFF

## State
`unit` option implemented and finished (index.js, index.d.ts, readme.md, test.js, index.test-d.ts). `npm test` (xo + ava + tsd) passes.

## Decisions
- `unit` is validated against the unit list picked by `bits`/`binary`; anything else (wrong system, wrong case, non-string) throws TypeError.
- A forced unit skips the automatic boundary corrections (the `number < 1` step-down and the round-up to the next unit), since those would change the unit the user asked for. So `999999` bytes with `unit: 'kB'` is `1000 kB`.
- Exponent selection moved into `pickExponent` to keep `prettyBytes` under xo's complexity limit.

## Policy (from user)
- New options must never throw on a bad value: ignore it and format as if the option was not passed (a stale saved pref crashed the dashboard after the `unit` release).
- `unit` already ships with its TypeError, so it is left alone until the next major.

## significantDigits (done)
- `significantDigits` replaces the hard-coded 3 in the default rounding; ignored when a fraction-digit option is set.
- Per the policy above it never throws: anything but an integer 1..100 (the `toPrecision` range) falls back to 3 (`resolveSignificantDigits`). Tests cover this. `npm test` passes.

## Latest
- Added a `{bits: true, unit: 'Mbit'}` example to the readme `unit` section and a matching test (`1_337_000` -> `1.34 Mbit`).
