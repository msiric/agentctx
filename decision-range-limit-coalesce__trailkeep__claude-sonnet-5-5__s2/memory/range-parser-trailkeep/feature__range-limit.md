# feature/range-limit

Branch: feature/range-limit · Repo: local__range-parser-2115724198 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: Decision for the `limit` option on rangeParser (branch feature/range-limit): when a header has more ranges than `limit`, return ONE range from the lowest start to the highest end (coalesce, don't return -1/-2 and don't truncate). Reason: the CDN can cache single-range responses but not multipart ones, and video players tolerate a few extra bytes. Nothing written yet; implement next session. Open points: count valid ranges vs raw pieces vs post-combine; default stays unlimited; keep .type on the result; README/HISTORY/tests to update.
- 2026-11-05: limit option implemented (index.js, tests, README, HISTORY). Resolved open points: count valid ranges AFTER combine (if enabled), since combining shrinks the count; invalid/unsatisfiable pieces never count; limit must be a number >=1 else ignored (unlimited default); result keeps .type; -1/-2 behavior unchanged.

