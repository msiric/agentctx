# HANDOFF

## State
Added opt-in `requireUnit` option: `parse(str, { requireUnit: true })` returns NaN for unitless strings. `ms(str, opts)` forwards options to `parse`. Tests in `src/parse.test.ts`, README updated. tsc + jest pass (100% coverage). Not committed.

## Decisions
- Option lives on the shared `Options` interface (alongside `long`) so `ms()` can forward it; default is off, so behaviour is unchanged.
- Returns NaN (not throw) to match how unparseable strings are already treated.
- `parseStrict` left unchanged (single-arg); not asked for.

## Failed approaches
None.
