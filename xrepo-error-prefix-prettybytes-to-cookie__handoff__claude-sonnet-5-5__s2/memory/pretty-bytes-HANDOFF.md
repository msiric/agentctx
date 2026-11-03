# Handoff

## State
`maxUnit` option added (index.js, index.d.ts, readme.md, test.js, index.test-d.ts). `npm test` (xo, ava, tsd) passes. Not committed.

## Decisions
- `maxUnit` caps the exponent: `getMaxExponent` looks the name up in the unit list chosen by `bits`/`binary`; replaces the old `UNITS.length - 1` cap in both the initial exponent and the post-rounding bump.
- Unit names are case-sensitive; a name not in the selected system (e.g. `GiB` without `binary`) or a non-string throws TypeError. `undefined` means no cap.
- Validation runs before any formatting, so it throws even for inputs like 0.
- Typed as `string` (not a union), since the valid set depends on `bits`/`binary`.

## Failed approaches
- None. xo's no-mixed-operators required parentheses around `**` in tests.

## Error prefix
The new maxUnit error message starts with `pretty-bytes: ` (user convention across their packages, to identify the source dependency). Existing messages deliberately left unprefixed for now, at the user's request.
