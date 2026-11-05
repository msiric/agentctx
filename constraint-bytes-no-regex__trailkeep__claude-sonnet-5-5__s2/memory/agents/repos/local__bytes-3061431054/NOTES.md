# Private notes: local__bytes-3061431054

- 2026-11-05: No new or changed regexes in index.js without AppSec sign-off (queue ~3 weeks); do new parsing with plain string handling. Reason: AppSec ReDoS audit; existing regexes measured safe (parse linear, format regexes only see bounded toFixed output).
