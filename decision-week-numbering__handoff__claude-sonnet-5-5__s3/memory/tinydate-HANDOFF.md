# HANDOFF

## Task
Add a `{WW}` week-number token to tinydate (branch `feat/week-number`), built in steps.

## Decisions
- Week system: match finance's Excel `WEEKNUM(date, 2)`. Weeks start Monday, and week 1 is the week containing Jan 1. This is NOT ISO 8601 (earlier ISO recommendation dropped). Jan 1 is always week 1, so there is no week 0 and no week-year mismatch. Dec 29-31 can be week 53 or 54 under this system.
- Work is split: `{DDD}` first, for separate review. `{WW}` comes after and will build on it.

## State
- Done (uncommitted, awaiting review): `{DDD}` day of year, zero-padded to 3 digits.
  - `src/index.js`: the DDD function uses `Date.UTC` differences, so DST shifts can't skew the count.
  - `index.d.ts`: added to `Defaults`.
  - `readme.md`: documented.
  - `test/index.js`: first/last day, leap year, leap day, Mar 1, around DST start and end, 23:59:59.
- `npm test` passes (30/30) under TZ=America/New_York and TZ=Asia/Tokyo.
- Done (uncommitted): `{WW}` in `src/index.js` (shares a `dayOfYear` helper with DDD), `index.d.ts`, `readme.md`, and 12 tests in `test/index.js` (Jan 1 on Sun/Mon/Fri, week boundaries, Dec 31 = 53, DST dates).
- `npm test` passes (42/42) under TZ=America/New_York and TZ=Asia/Tokyo.
- Nothing committed yet.

## Notes for `{WW}`
- Can reuse the day-of-year calculation. With Monday = 0, offset = (weekday of Jan 1), week = floor((doy - 1 + offset) / 7) + 1.
- The existing padding trick (`'00' + n).slice(-key.length)` works for a 2-char key.

## Failed approaches
- First draft of two test expectations was wrong (default date May 1 2017 is week 19, Nov 6 2017 is week 46); I had miscounted by hand. Code was right, tests corrected.
