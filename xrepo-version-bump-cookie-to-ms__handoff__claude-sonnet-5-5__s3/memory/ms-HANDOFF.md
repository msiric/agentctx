# HANDOFF

## State
Added microsecond unit to `ms`/`parse`: `us`, `µs` (U+00B5), `μs` (U+03BC), `microsecond(s)`, case-insensitive. Value = n / 1000. Types (`Microseconds`, `Unit`), README and tests (parse, parse-strict, index) updated. tsc, jest (100% coverage), biome pass.

## Decisions
- Accepted both micro sign and Greek mu: uppercasing `µ` in the regex yields Greek capital Mu, whose lowercase is U+03BC, so the switch needs both forms.
- Also accepted `us` (ASCII) as a convenience alongside the requested spellings.
- Mixed-case (`MicroSeconds`) and `µS` work at runtime via `parse` but are rejected by `StringValue` types (same as existing units), so only `parse` tests cover them.
- Formatting (number -> string) unchanged; sub-ms values still print as `ms`.
