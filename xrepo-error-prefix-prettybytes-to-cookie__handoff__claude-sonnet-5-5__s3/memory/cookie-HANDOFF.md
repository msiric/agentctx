# Handoff

## State
`stringifySetCookie` now throws `TypeError` (`option maxAge is invalid: ... exceeds 400 days`) when `maxAge` > 34,560,000 s. Implemented in `src/index.ts` (`maxMaxAge` constant + check + JSDoc), documented in README `maxAge` section, tests in `src/stringify-set-cookie.spec.ts` (over limit throws, exactly 400 days allowed). Tests and tsc pass. Not committed.

## Decisions
- Limit is inclusive (exactly 400 days OK), since browsers cap at 400 days.
- Reused the existing "option maxAge is invalid" message prefix so the existing error pattern holds.
- `parseSetCookie` is unchanged: it parses what servers send and shouldn't throw.

## Failed approaches
None.
