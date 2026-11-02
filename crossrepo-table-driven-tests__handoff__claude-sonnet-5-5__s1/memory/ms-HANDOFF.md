# HANDOFF

## State
Microsecond units added to `ms.parse` (`us`, `µs`, `microsecond`, `microseconds`); `ms("500us")` = 0.5.
Done: src/index.ts (type, regex, switch), README unit list, tests in src/parse.test.ts. tsc + jest pass, 100% coverage. Not committed.

## Decisions
- Regex is case-insensitive; uppercasing `µ` (U+00B5) gives Greek `Μ`, which lowercases to `μ` (U+03BC), not `µ`. So the switch handles both `µs` and `μs`, otherwise `500 Μs`/`µS` would throw.
- Formatting (`ms(0.5)`) unchanged: still outputs `0.5ms`; parsing only.
