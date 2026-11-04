# Handoff

## State
Done: `parse(str, { requireUnit: true })` returns NaN for unit-less strings ("30", "1.5", "-5"). Default (omitted/false) unchanged. Tests added in `src/parse.test.ts`; README example added. tsc, jest (node), biome lint pass. Edge-runtime tests not run separately.

## Decisions
- Option lives on `parse` only (new `ParseOptions`), not on `ms()` / `parseStrict`, to keep scope minimal. `ms()` string path still calls `parse(value)` without options.
- Returns NaN (not throw) to match the existing "can't be parsed" contract.

## Failed approaches
None.

## Conventions (user preference)
- Never use positional boolean parameters; use an options object (e.g. `parse(str, { requireUnit: true })`).
