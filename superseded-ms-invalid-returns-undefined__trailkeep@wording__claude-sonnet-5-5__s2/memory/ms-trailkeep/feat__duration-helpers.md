# feat/duration-helpers

Branch: feat/duration-helpers · Repo: local__ms-1348162504 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: parseCompound must never return NaN: bad input (empty, 'abc', '1h foo', unknown unit) throws TypeError including JSON.stringify(input). Reason: user once had NaN reach setTimeout and it was hard to track down. (parse itself still returns NaN; that's unchanged.)
- 2026-11-05: parseCompound keeps throwing TypeError (published API); the undefined-on-bad-input rule applies only to later helpers.
- 2026-11-05: parseClock (added, returns number | undefined per the repo rule): my choices, not the user's: m:ss allows any number of leading digits ('90:00' valid); seconds and minutes-with-hours must be two digits and <60; whitespace trimmed; input >100 chars or non-string gives undefined. README section for parseClock not yet written (offered, user hasn't answered).

