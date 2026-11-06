# Private notes: local__pretty-bytes-2442101067

- 2026-11-06: Rule from user: new options must never throw on a bad value; ignore it and format as if the option wasn't passed. Reason: a stale saved pref (unit: 'KB') crashed the storage dashboard file table for all users with it. Exception: the shipped 'unit' option keeps its TypeError until the next major; leave it alone.
