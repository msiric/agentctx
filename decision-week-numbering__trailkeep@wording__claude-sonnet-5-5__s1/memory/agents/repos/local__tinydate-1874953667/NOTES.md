# Private notes: local__tinydate-1874953667

- 2026-11-05: Week numbers ({WW}, planned) must match finance's Excel WEEKNUM(date, 2): weeks start Monday, week 1 is the week containing Jan 1 (NOT ISO 8601). User decision, driven by finance spreadsheets. {DDD} day-of-year token (zero-padded to 3) lands first, separately, for review; week token builds on it.
