# HANDOFF

## State
Added `dotCase` (src/index.ts, `DotCase` type in src/types.ts), tests in test/scule.test.ts, README section. Implemented as `kebabCase(str, ".")`, mirroring snakeCase/flatCase.

## Decisions
- Reused kebabCase with "." joiner for consistency; no new options.

## Failed approaches
None.
