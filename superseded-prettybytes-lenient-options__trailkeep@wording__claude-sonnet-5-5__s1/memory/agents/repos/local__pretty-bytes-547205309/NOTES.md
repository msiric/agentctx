# Private notes: local__pretty-bytes-547205309

- 2026-11-05: User rule: new options must never throw on a bad value; ignore it and format as if the option wasn't passed. Reason: the storage dashboard passes saved user prefs straight into prettyBytes, and a stale 'unit: KB' pref crashed the file table. Exception: 'unit' already shipped with its TypeError, so leave it until the next major (then make it ignore bad values too).
