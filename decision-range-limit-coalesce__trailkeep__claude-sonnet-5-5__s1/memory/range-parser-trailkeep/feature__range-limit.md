# feature/range-limit

Branch: feature/range-limit · Repo: local__range-parser-3000413686 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: Decision for the rangeParser `limit` option: when a header has more ranges than `limit`, don't reject or truncate. Merge them into ONE range from the lowest start to the highest end (the covering range). Reason: the CDN can cache single-range responses but not multipart ones, and video players tolerate a few extra bytes. Rejected: return -2, return -1, truncate to first N, throw, new return code. Open questions still to settle: count raw pieces vs post-combine ranges, and whether to bail early before split(','). Not written yet; implementation is next session. Code is in index.js, with the README Options section and tests in test/.
- 2026-11-05: rangeParser limit implemented (index.js coverRanges, README, tests). Settled open questions: limit counts valid ranges AFTER combine (invalid/unsatisfiable not counted); no early bail before split(',') — kept simple, so parsing cost is not bounded by limit. limit < 1 or non-numeric is ignored. Reason: simplest semantics matching 'ranges we take'; revisit early bail if header-size DoS matters.

