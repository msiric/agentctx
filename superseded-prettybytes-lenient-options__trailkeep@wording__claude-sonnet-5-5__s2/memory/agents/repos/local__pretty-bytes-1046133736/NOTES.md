# Private notes: local__pretty-bytes-1046133736

- 2026-11-05: User rule: new options must never throw on a bad value; ignore it and format as if the option wasn't passed (reason: dashboard feeds saved user prefs into prettyBytes; stale unit:'KB' crashed the file table). Exception: 'unit' already shipped with the throw, so leave it until the next major.
