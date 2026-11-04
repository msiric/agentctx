# Private notes: local__pretty-bytes-1470974862

- 2026-11-04: New options must never throw on a bad value: ignore it and format as if the option wasn't passed (saved user prefs go straight into prettyBytes; stale unit:'KB' crashed the dashboard). unit already throws; leave until next major.
