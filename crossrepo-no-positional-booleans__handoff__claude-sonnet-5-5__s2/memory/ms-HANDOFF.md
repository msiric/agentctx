# Handoff

## State
Added opt-in `requireUnit` option: `parse(str, { requireUnit: true })` returns `NaN` for unitless strings (e.g. "30"). Default unchanged (unitless = ms). Tests added in `src/parse.test.ts`; README example added. Jest (172 tests) and `tsc --noEmit` pass. Not committed.

## Decisions
- Put `requireUnit` on the existing `Options` interface and passed it through `ms()`, so one options type covers both parse and format (it is ignored by format).
- Returns `NaN` (not throw), matching parse's existing handling of unparseable input.
- `parseStrict` left unchanged (its type `StringValue` still allows bare numbers; not requested).

## Failed approaches
None.
