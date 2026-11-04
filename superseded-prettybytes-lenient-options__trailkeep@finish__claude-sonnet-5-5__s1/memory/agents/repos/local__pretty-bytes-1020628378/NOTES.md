# Private notes: local__pretty-bytes-1020628378

- 2026-11-04: New prettyBytes options must never throw on a bad value: ignore it and format as if the option wasn't passed. Reason: the dashboard feeds saved user prefs straight in, and a stale unit: 'KB' crashed the file table. 'unit' already shipped with a throw; leave it until the next major.
