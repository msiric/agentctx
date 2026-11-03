# Handoff

## State
`stringifySetCookie` now throws a `TypeError` when `maxAge` > 34,560,000 s (400 days). Implemented in `src/index.ts` (`maxMaxAge` constant), documented in the JSDoc and README (`maxAge` section), tests added in `src/stringify-set-cookie.spec.ts` (over limit throws, exactly 400 days allowed). All tests pass. Not committed.

## Decisions
- Limit is inclusive (exactly 400 days is allowed), since browsers cap at 400 days and don't shorten that.
- Only stringify throws; `parseSetCookie` is unchanged so incoming headers are still parsed as-is.

## Failed approaches
None.
