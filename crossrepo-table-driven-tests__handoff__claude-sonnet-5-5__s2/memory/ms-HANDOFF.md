# Handoff: microsecond support

State: done. `us`, `µs`, `microsecond(s)` parse to ms (`n / 1000`) in `src/index.ts`; `Microseconds` type added to `Unit`; README type list updated; tests in `parse.test.ts` and `parse-strict.test.ts`. tsc and jest pass (100% coverage).

Decisions:
- The regex is case-insensitive, so `Μs`/`µs`/`μs` all match; `toLowerCase` can yield U+03BC (Greek mu) as well as U+00B5 (micro sign). Both are handled in the switch.
- Formatting (`ms(0.5)`) is unchanged: still outputs `0.5ms`. Not requested.
- The `Μs` (Greek capital) uppercase form isn't in the `StringValue` type (parseStrict). Only `Capitalize`/`Uppercase` of `µs` are.
