# Private notes: local__bytes-1784580938

- 2026-11-06: Rule agreed with AppSec (ReDoS audit): do not add or change regexes in index.js without AppSec sign-off (their queue is ~3 weeks). Any new parsing needed in index.js must use plain string handling instead of regexes.
