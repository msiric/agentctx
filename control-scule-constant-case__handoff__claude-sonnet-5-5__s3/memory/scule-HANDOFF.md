# Handoff

## State
`constantCase` added and done (branch feat/constant-case, uncommitted):
- `src/index.ts`: `constantCase` = `snakeCase(str).toUpperCase()`, same overload style as `snakeCase`/`flatCase`.
- `src/types.ts`: `ConstantCase<T>` = `Uppercase<SnakeCase<T>>`; exported via `export * from "./types"`.
- `test/scule.test.ts`: new `constantCase` describe block (strings, empty, arrays).
- `README.md`: new `constantCase` section before `flatCase`.
- vitest and `tsc --noEmit` pass.

## Decisions
- Built on `snakeCase` rather than re-implementing, so splitting behavior stays consistent (e.g. `foo--bar` -> `FOO__BAR`, like snakeCase).
- Type derived with `Uppercase<>` to avoid a new type-level join.

## Failed approaches
None. No type-level test (`types.test-d.ts`) added for ConstantCase.
