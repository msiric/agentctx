# Private notes: local__tinydate-1674482580

- 2026-11-04: Week token {WW} must match Excel WEEKNUM(date, 2) (Monday start, week 1 contains Jan 1), not ISO 8601: finance's spreadsheets use it. {DDD} (day-of-year, zero-padded to 3) is being added first, separately, for review.
