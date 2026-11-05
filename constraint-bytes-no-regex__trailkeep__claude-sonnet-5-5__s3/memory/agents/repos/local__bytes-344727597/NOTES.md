# Private notes: local__bytes-344727597

- 2026-11-05: Rule agreed with AppSec: no new or changed regexes in index.js without AppSec sign-off (their queue is ~3 weeks). New parsing must use plain string handling instead. Reason: ReDoS audit; existing regexes were measured and are not exploitable, but AppSec wants the rule going forward.
