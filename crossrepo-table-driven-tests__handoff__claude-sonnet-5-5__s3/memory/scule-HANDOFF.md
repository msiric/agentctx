# HANDOFF

## State
`dotCase` added (src/index.ts, `DotCase` type in src/types.ts), README section, tests in test/scule.test.ts. Implemented as `kebabCase(str, ".")`, same as snakeCase/flatCase.

## Decisions
- Reused kebabCase with "." joiner for consistency with sibling functions.
