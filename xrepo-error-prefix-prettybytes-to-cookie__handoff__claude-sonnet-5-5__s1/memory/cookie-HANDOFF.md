# Handoff

## State
`stringifySetCookie` now throws a `TypeError` when `maxAge` > 34,560,000 s (400 days). Done: `src/index.ts`, tests in `src/stringify-set-cookie.spec.ts`, README `maxAge` section. Tests and tsc pass.

## Decisions
- Limit is inclusive (exactly 400 days allowed), per the request ("over 400 days").
- Message starts with `option maxAge is invalid` to match the existing maxAge errors.
- Only stringify is affected. `parseSetCookie` still accepts any value, since it reads headers from other servers.

## Failed approaches
None.
