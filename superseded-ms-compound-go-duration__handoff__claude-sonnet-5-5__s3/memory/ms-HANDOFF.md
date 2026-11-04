# Handoff

## State
`compound` option added to `format`/`ms` (src/index.ts, `fmtCompound`). `format(5400000, { compound: true })` → `1h 30m`. Tests in src/format.test.ts and src/index.test.ts, README section added. Committed as 64cf040 on feat/compound-format (not pushed, no PR). HANDOFF.md itself is deliberately left untracked.

`parse()` now trims leading/trailing whitespace before matching (`' 2d'`, `'1.5h '` work; whitespace-only → NaN). Change is in src/index.ts + test in src/parse.test.ts, committed as c53f6e9 (not pushed). Jest and tsc pass. The 1..99 length check still applies to the untrimmed input.

## Done: Go-compatible compound output
`fmtCompound` now emits no spaces, hours as largest unit (`25h30m`, `192h`). Tests (format, index) and README updated; Jest (100% coverage) and tsc pass. Negative = single leading `-` (Go-valid); `0s` for <1s (Go-valid). Committed on feat/compound-format, not pushed, no PR.

## Decisions
- Units h/m/s only (no days, for Go compatibility); ms dropped by flooring total seconds (truncates, doesn't round).
- Negative: single leading `-`, applied to the whole string.
- Result under 1s (including negatives like -500) → `0s`, never `-0s`. Not specified by the user; chosen so output is never empty.
- `compound` takes precedence over `long` if both are set.
- Whitespace tolerance done via `str.trim()` at match time rather than changing the regex, so the existing internal-space support (`'1   s'`) is untouched.

## Failed approaches
None.
