# Handoff

## State
`maxUnit` option implemented in index.js, typed in index.d.ts (+ index.test-d.ts), documented in readme.md, tested in test.js. `npm test` (xo, ava, tsd) passes.

## Decisions
- `maxUnit` is validated against the unit list selected by `bits`/`binary` (case-sensitive); unknown units throw TypeError. `undefined` means no cap.
- Cap replaces `UNITS.length - 1` both in the initial exponent clamp and in the rounding bump (so 999999999999 B with GB gives `1000 GB`, not a nonexistent larger unit).
- Lookup lives in `getMaxExponent` to keep `prettyBytes` under xo's complexity limit.
- Typed as `string` (not a union) since valid values depend on `bits`/`binary`.

## Failed approaches
- A readme example showing the TypeError broke the "documented examples are accurate" test (it evaluates every `//=>` block), so that case is prose only.

## Error message prefix
The maxUnit error starts with `pretty-bytes: ` (user convention across their packages, so the source dependency is identifiable when thrown deep in an app). Existing error messages intentionally left unprefixed for now, at the user's request.
