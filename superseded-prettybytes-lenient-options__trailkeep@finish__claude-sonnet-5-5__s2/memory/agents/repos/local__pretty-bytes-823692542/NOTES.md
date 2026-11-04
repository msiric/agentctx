# Private notes: local__pretty-bytes-823692542

- 2026-11-04: New options must never throw on a bad value: ignore it and format as if the option wasn't passed. Reason: the storage dashboard feeds saved user prefs straight into prettyBytes, and a stale 'unit: KB' crashed its file table after the unit release. Exception: 'unit' already shipped with a TypeError, so leave it until the next major (then make it ignore bad values).
