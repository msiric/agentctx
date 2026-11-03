# Private notes: local__pretty-bytes-996746065

- 2026-11-03: Rule: new prettyBytes options must never throw on a bad value; ignore it and format as if not passed (stale saved prefs crashed the dashboard). Existing 'unit' option still throws; leave until next major.
