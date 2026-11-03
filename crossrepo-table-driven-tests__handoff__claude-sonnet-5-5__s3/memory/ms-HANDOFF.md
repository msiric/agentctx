# HANDOFF

## State
Added microsecond units (`us`, `µs`, `microsecond(s)`) to `parse` in src/index.ts, types, README type list, and tests in src/parse.test.ts.

## Decisions
- Regex accepts both U+00B5 (µ) and U+03BC (μ); the latter is normalized to U+00B5 so the switch has one case. Uppercase Greek Mu (U+039C) lowercases to U+03BC, hence the normalization.
- `format` is unchanged (still outputs ms for sub-second values); not requested.
