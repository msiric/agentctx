# HANDOFF

## State
`constantCase` added and complete: src/index.ts (function), src/types.ts (`ConstantCase` type), tests in test/scule.test.ts, README section. Vitest (69) and `tsc --noEmit` pass.

## Decisions
- Implemented as `snakeCase(str).toUpperCase()`, typed as `Uppercase<SnakeCase<T>>`, so splitting behaviour matches snakeCase exactly.
- No `normalize` option (not needed; output is all uppercase).

## Failed approaches
None.
