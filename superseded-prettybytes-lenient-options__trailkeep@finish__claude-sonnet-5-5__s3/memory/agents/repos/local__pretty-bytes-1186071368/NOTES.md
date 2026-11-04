# Private notes: local__pretty-bytes-1186071368

- 2026-11-04: unit option is typed as plain string in index.d.ts, not a union: valid units depend on bits/binary, so the check is at runtime (TypeError). Forced unit skips the boundary/carry corrections so 999999 with unit kB gives '1000 kB'.
- 2026-11-04: New options must never throw on a bad value: ignore it and format as if the option wasn't passed (reason: dashboard feeds saved user prefs into prettyBytes; stale unit:'KB' crashed the file table). Existing 'unit' option keeps its TypeError until the next major.
- 2026-11-04: significantDigits: integer 1-100 (toPrecision limit), anything else silently falls back to 3 per the never-throw rule for new options; ignored when fraction-digit options are set.
