# HANDOFF

## Task
Add a `{WW}` week-number token to tinydate (branch `feat/week-number`), matching finance's Excel `WEEKNUM(date, 2)`: weeks start Monday, week 1 is the week containing Jan 1 (NOT ISO 8601).

## State
- Step 1 DONE (awaiting user review, uncommitted): `{DDD}` day-of-year token, zero-padded to 3. Touches `src/index.js`, `test/index.js`, `readme.md`, `index.d.ts`. 29 tests pass, including with `TZ=America/New_York`.
- Step 2 DONE (uncommitted): `{WW}` in `src/index.js`, with tests, readme entry and `index.d.ts` type. 41 tests pass, also with `TZ=America/New_York`. The user said to carry on, so I did not wait for a separate DDD review. Nothing is committed yet.

## Decisions
- `{WW}` follows WEEKNUM(date, 2), per finance. Decided by the user, replacing my earlier ISO proposal.
- Week-year token: not needed for this rule. Week 1 contains Jan 1, so the week number never belongs to a different year. Late-December days can be week 53 or 54 depending on weekday, but Excel does the same.
- `{DDD}` uses `Date.UTC` on the local year/month/date fields, then `Math.round(diff / 864e5) + 1`. This avoids DST skew (a local-time diff would be off by an hour on DST days) and stays local-time consistent with the other tokens.
- Padding reuses the existing `('00' + n).slice(-key.length)` mechanism, so no padding code was added.
- Tests import `../dist/tinydate`, so run `npm run build` before `npm test`.

- `{WW}` = floor((dayOfYear - 1 + jan1MondayIndex) / 7) + 1, where jan1MondayIndex = (Jan 1 getDay() + 6) % 7. The `dayOfYear` helper is now shared by DDD and WW.

## Failed approaches
- My first test expected Dec 31, 2017 to be week 54. That was my arithmetic error: it is 53. Week 54 needs a leap year starting on Sunday, e.g. Dec 31, 2012. The code was correct and the test was fixed.
