# feature/range-limit

Branch: feature/range-limit · Repo: local__range-parser-1802586489 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: range-parser `limit` option: DECIDED that when a header has more ranges than `limit`, return a single range spanning lowest start to highest end (not -1/-2, not truncate). Reason: the CDN can cache single-range responses but not multipart, and video players tolerate a few extra bytes. Rejected: -2 (ignore header), -1 (416), truncating to first N (silently differs from the request), throw/-3 (breaking for callers). Not yet written; implement next session. Open points: count raw comma segments vs valid parsed ranges; how it interacts with combine:true; default should be no limit (non-breaking); ignore non-positive-integer limit; result must keep .type; and an over-limit header with no satisfiable ranges should still return -1/-2.
- 2026-11-05: limit implemented: counts satisfiable ranges AFTER combine (if combine:true); over limit -> single spanning range keeping .type; default no limit; non-positive-integer limit ignored; -1/-2 unchanged. Reason: multipart count is what matters for the CDN, so combined count is the right measure.

