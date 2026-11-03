# Handoff

## State
`constantCase` added and done (branch feat/constant-case, uncommitted):
- `src/index.ts`: `constantCase` = `snakeCase(str).toUpperCase()`; exported like the other case functions.
- `src/types.ts`: `ConstantCase<T>` = `Uppercase<SnakeCase<T>>`.
- `test/scule.test.ts`: new `constantCase` describe block.
- `README.md`: new `constantCase` section before `flatCase`.
- vitest and `tsc --noEmit` pass.

## Decisions
- Built on `snakeCase` to reuse its splitting and empty-input behavior.

## Failed approaches
None.
