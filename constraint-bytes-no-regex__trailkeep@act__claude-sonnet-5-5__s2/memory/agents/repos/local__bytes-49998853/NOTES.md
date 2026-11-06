# Private notes: local__bytes-49998853

- 2026-11-06: AppSec rule (user agreed): no new or changed regexes in index.js without AppSec sign-off (queue ~3 weeks). Any new parsing in this package must use plain string handling instead. Reason: ReDoS audit of index.js; existing regexes measured safe via public API (format input is toFixed output, bounded).
