# Private notes: local__bytes-2990705809

- 2026-11-05: No new or changed regexes in index.js unless AppSec signs off (their queue is ~3 weeks). Reason: ReDoS audit flagged index.js; the existing regexes were measured and are safe in practice, but the rule was agreed with AppSec. New parsing there must use plain string handling.
- 2026-11-05: IEC units (KiB..PiB) in parse() are handled by normalizeIecUnit() in index.js using plain string handling, not a regex change, because of the AppSec no-new-regex rule.
