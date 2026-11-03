# Handoff

## State
`maxUnit` option implemented in `index.js`, with types (`index.d.ts`, `index.test-d.ts`), readme section and tests (`test.js`). `npm test` (xo, ava, tsd) passes. Nothing is committed.

## Decisions
- Units are validated against the system chosen by `bits`/`binary` (`getMaxExponent`), so `GiB` without `binary` throws a `TypeError`. `undefined` means no cap.
- The cap replaces `UNITS.length - 1` in both places that bound the exponent: the initial exponent and the bump after rounding (`999_999_999_999` with `maxUnit: 'GB'` gives `1000 GB`, not `1 TB`).
- Typed as `string`, not a union, because the valid set depends on `bits`/`binary`.
- A capped bigint past the number range goes through the existing exact-quotient path, which needed no change.

## Failed approaches
- First test used `2 * 1024 ** 4`, which failed the xo `no-mixed-operators` rule. Parenthesized it. The bigint literal was written out in full for the same reason.

## Error prefix
The `maxUnit` error message starts with `pretty-bytes: ` so a throw deep in an app names the dependency. Existing messages are deliberately left unprefixed for now (user's call).
