# feat/week-number

Branch: feat/week-number · Repo: local__tinydate-1008554459 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: Week token {WW} must match Excel WEEKNUM(date, 2): weeks start Monday, week 1 = the week containing Jan 1 (NOT ISO 8601). Reason: finance's spreadsheets use it. User chose this; DDD (day-of-year, zero-padded to 3) is being added first as a separate change for separate review, and the week token will build on it.
- 2026-11-06: DDD token is implemented but uncommitted, awaiting the user's review; do not start {WW} until they've reviewed it. Not done (my choice to defer): the '349B' size claim in readme.md and package.json was not re-checked after adding DDD. Plan for WW (mine, unverified): week = floor((DDD - 1 + jan1MondayBasedWeekday) / 7) + 1, with Monday=0.
- 2026-11-06: WW {WW} implemented on top of shared doy() helper (src/index.js), tests+readme+d.ts done; tests pass in several TZs. User said 'carry on' so I (assistant) treated DDD as reviewed-enough to proceed; DDD+WW still uncommitted. '349B' size claim in readme.md/package.json NOT updated: gzipped min is now ~520B after DDD+WW (my measurement), needs user decision.

