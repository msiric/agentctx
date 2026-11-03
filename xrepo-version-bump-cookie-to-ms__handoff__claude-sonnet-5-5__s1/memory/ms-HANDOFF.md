# HANDOFF

## State
Added microsecond support to `parse` / `ms` (`us`, `µs`, `microsecond(s)`, any case). Types, README unit list and tests (index/parse/parse-strict) updated. tsc, jest (100% coverage) and biome pass. Not committed.

## Decisions
- Value is `n / 1000` (not `n * 0.001`) to avoid float error.
- Regex accepts both micro sign U+00B5 and Greek mu U+03BC; `/i` also matches Greek capital Mu. The unit is normalized U+03BC -> U+00B5 after lowercasing so one switch case covers all.
- `StringValue` type only lists `µs` (U+00B5) lowercase; `Capitalize` gives `Μs`, so that is type-valid too. Greek `μs` is runtime-only (`@ts-expect-error` in tests).
- Formatting (`ms(0.5)`) unchanged; user asked only for parsing.

## Failed
- First attempt at tests put `@ts-expect-error` on cases that were valid types (`US`, `Μs`); removed.
