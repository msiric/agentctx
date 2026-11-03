# HANDOFF

## State
`parseCompound(str)` and `parseClock(str)` added to `src/index.ts` (exported). Tests in `src/parse-compound.test.ts`.
Comma support and README done. Jest (100% coverage threshold), tsc, biome lint/format all pass. Not committed.

## Decisions
- The whole string must match `piece (\s*,?\s*piece)*` (anchored, with optional surrounding whitespace), then pieces are extracted with a global regex. Separators: whitespace, a single comma, or nothing (`1h30m`, `1h 30m`, `1h, 30m`). Leading/trailing/double commas throw. Change is strictly additive: everything valid in 4.1.0-canary.1 is still valid and returns the same value (it already shipped, dashboard team uses it).
- Each piece goes through `parse`; a NaN result for any piece throws. A piece without a unit (e.g. `1h 30`) is invalid rather than defaulting to ms, since it's ambiguous.
- All invalid input (empty, >100 chars, non-string, junk, bad unit) throws `TypeError` with `JSON.stringify(input)` in the message. User request: NaN once reached setTimeout and was hard to trace, so never return NaN. (Differs from `parse`, which returns NaN.)

- Convention for FUTURE helpers (user decision, after issue-tracker feedback that throwing forces try/catch in config loaders): return `undefined` on bad input, typed `number | undefined` (or the equivalent), so TypeScript forces callers to handle it. Never NaN (the original reason still stands). `parseCompound` stays throwing because it is already published in 4.1.0-canary.1; do not change it. Don't add a non-throwing variant of it unless asked.

- `parseClock(str): number | undefined` added (exported, tests in `src/parse-clock.test.ts`, README "Clock Strings"). Follows the undefined-on-bad-input convention. Strict format: `m:ss` (minutes any digits) or `h:mm:ss`; seconds and h:mm:ss minutes must be two digits <60. No whitespace trimming, no negatives, no fractional seconds (can be added if wanted).

## Failed approaches
None.

## Open
Nothing. README has a "Compound Durations" section under Advanced Usage. Not committed; version bump/release is the user's call.
