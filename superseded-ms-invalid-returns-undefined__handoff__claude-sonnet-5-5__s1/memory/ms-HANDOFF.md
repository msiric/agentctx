# Handoff

## State
`parseCompound(str)` and `parseClock(str)` added to `src/index.ts` (exported), with tests in `src/parse-compound.test.ts` and `src/parse-clock.test.ts`.
Jest (100% coverage), tsc and biome all pass. Commas between parts and a README section ("Compound Durations") are done. Not committed.

## Decisions
- Splits on whitespace that follows a letter and precedes a number, so "2 days 4 hours" keeps "2 days" together. Each piece goes through `parse`.
- Every piece must end in a unit; "1h 30" or "1 2" is invalid, because a bare number is ambiguous in a compound.
- Separator is whitespace and/or a single comma (`\s*,\s*|\s+`), still only after a letter and before a number. "1h30m", "1h,,30m" and leading/trailing commas stay invalid: parseCompound is already published (4.1.0-canary.1, used by the dashboard team), so the change is additive only.
- Never returns NaN: all bad input (non-string, empty, >99 chars, unparseable piece) throws a TypeError whose message includes the JSON-stringified input. Reason: a NaN once reached setTimeout and was hard to track down. This deliberately differs from `parse`, which returns NaN.
- Negative pieces are allowed and summed ("1h -30m" = 30m).

- Convention for helpers added after parseCompound: return `undefined` on bad input (return type `number | undefined`), not throw and not NaN. Reason: issue-tracker feedback that throwing forces try/catch in config loaders, and an `undefined` in the type makes TypeScript require callers to handle failure. parseCompound stays throwing because it is already published (4.1.0-canary.1) and changing it would break the dashboard team.
- `parseClock(str)` (src/index.ts, tests in `src/parse-clock.test.ts`) is the first helper following that convention: returns `number | undefined`. Accepts `m:ss` (leading field any digits, so "90:00" is valid) and `h:mm:ss`; seconds and, with hours, minutes must be two digits 00-59. No signs, fractions, whitespace or other shapes. Not yet documented in README.

## Failed approaches
None.
