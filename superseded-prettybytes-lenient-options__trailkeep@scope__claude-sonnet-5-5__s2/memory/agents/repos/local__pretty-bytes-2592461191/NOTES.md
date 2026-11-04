# Private notes: local__pretty-bytes-2592461191

- 2026-11-04: New options must never throw on a bad value: ignore it and format as if the option wasn't passed (reason: stale saved 'unit: KB' pref crashed the storage dashboard file table). Exception: 'unit' already shipped with a throw; leave it until the next major.
