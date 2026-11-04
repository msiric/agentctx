# Private notes: local__tinydate-3740969531

- 2026-11-04: Week token {WW} must match Excel WEEKNUM(date, 2): weeks start Monday, week 1 is the week containing Jan 1 (NOT ISO 8601). Reason: finance's spreadsheets use it. {DDD} day-of-year (zero-padded to 3) is being added first as a separate reviewable change; the week token builds on it.
