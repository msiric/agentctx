# HANDOFF

## State
Microsecond parsing added to `ms`/`parse`/`parseStrict` (`src/index.ts`): `us`, `µs`, `microsecond(s)`, any case. `ms('500us') === 0.5`. Types (`Microseconds`, added to `Unit`), README and tests (index, parse, parse-strict) updated. tsc, jest (100% coverage) and biome pass. Not committed.

## Decisions
- Formatting is unchanged (sub-ms numbers still print as `ms`); only parsing was requested.
- `µ` has three code points: micro sign U+00B5, Greek mu U+03BC, capital Mu U+039C. The `/i` regex matches all three. `toLowerCase()` of the capital gives U+03BC, so the parser normalizes U+03BC to U+00B5 before the switch.
- The `StringValue` type only admits `µs` (U+00B5) and the TS-computed capitalized/uppercase forms (U+039C). Mixed-case or Greek-small-mu inputs are tested only in `parse.test.ts`, since they are not valid `StringValue`s.

## Failed
- First test draft used mixed-case/`μs` inputs in `ms()` and `parseStrict()` tests; tsc rejected them, so they were moved to `parse` tests only.
