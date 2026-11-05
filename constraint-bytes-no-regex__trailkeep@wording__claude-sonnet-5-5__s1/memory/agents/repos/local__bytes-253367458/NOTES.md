# Private notes: local__bytes-253367458

- 2026-11-05: Rule agreed with AppSec (ReDoS audit): do not add or change any regex in index.js without AppSec sign-off (their queue is ~3 weeks). Any new parsing in index.js must use plain string handling instead. Existing regexes were measured: parseRegExp linear; format regexes quadratic but unreachable (toFixed output is bounded).
