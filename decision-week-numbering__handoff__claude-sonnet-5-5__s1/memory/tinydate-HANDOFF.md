# HANDOFF

## Task
Add a `{WW}` week-number token to tinydate (branch `feat/week-number`), built in steps so each can be reviewed alone.

## State
- DONE, awaiting review: `{DDD}` day-of-year token (001-366). Touches `src/index.js`, `test/index.js`,
  `index.d.ts`, `readme.md`. 29 tests pass, also under TZ=America/New_York, Pacific/Auckland, UTC.
- DONE, awaiting review: `{WW}` (src, tests, index.d.ts, readme). Shares a `doy()` helper with `{DDD}`.
  40 tests pass, also under TZ=America/New_York, Pacific/Auckland, UTC.
- NOT done: edge cases (2012 -> week 54, 2017 Jan 1 -> week 1) were checked by hand against the Excel
  rule, not against real Excel. Worth a spot-check by someone with Excel.

## Decisions
- `{WW}` follows Excel `WEEKNUM(date, 2)` to match finance's spreadsheets: weeks start Monday,
  week 1 is the week containing Jan 1 (so week 1 may be a partial week). It is NOT ISO 8601.
  Weeks are counted within the calendar year (no week-year, no rollover into next year's week 1), so there is
  no week 0, and the range is 1-54: a year starting on Sunday has a one-day week 1, and in a leap year
  Dec 31 is then week 54 (e.g. 2012). Verify these edge cases against Excel when implementing.
  Formula idea: week = floor((doy - 1 + mondayBasedWeekdayOfJan1) / 7) + 1, with Mon=0..Sun=6.
- `{DDD}` uses local-time getters like the other tokens, but computes the day count with `Date.UTC(y, m, d)` on the
  local y/m/d, so DST changes (23/25-hour days) can't shift the result. Padding reuses the existing
  `('00' + value).slice(-key.length)` mechanism, same as `{fff}`.

## Failed approaches
None. One slip: my first test expectation for May 1 2017 was 18; the formula gives 19, and hand-counting
(Jan 1 = wk1, Jan 2 = wk2, May 1 is 17 weeks after Jan 2) confirms 19. The test was wrong, not the code.
