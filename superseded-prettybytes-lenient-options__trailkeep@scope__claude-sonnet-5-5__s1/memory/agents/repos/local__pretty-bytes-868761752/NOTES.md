# Private notes: local__pretty-bytes-868761752

- 2026-11-04: New options must never throw on a bad value: ignore it and format as if the option wasn't passed. Reason: dashboard feeds saved user prefs into prettyBytes and a stale unit:'KB' crashed the file table. The existing 'unit' throw stays until the next major.
