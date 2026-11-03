# Handoff

## State
`dotCase` added and done (branch feat/dot-case, uncommitted). Vitest (70 tests) and `tsc --noEmit` pass.
- `src/index.ts`: `dotCase` = `kebabCase(str, ".")`, same overload style as `snakeCase`/`flatCase`.
- `src/types.ts`: `DotCase` type (JoinByCase with "."), exported via `export * from "./types"`.
- `test/scule.test.ts`: dotCase tests; README has a `dotCase` section.

## Decisions
- Reused `kebabCase` with a joiner, like snakeCase. Empty segments are kept ("foo--bar" -> "foo..bar"), matching snakeCase, unlike flatCase which drops them.

- Tests: one `test.each` table per function (user preference, all projects). Array input is a row in the table, not a separate test.

## Failed approaches
None.
