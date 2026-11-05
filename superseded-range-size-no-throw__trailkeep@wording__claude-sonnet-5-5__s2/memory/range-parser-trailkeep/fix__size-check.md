# fix/size-check

Branch: fix/size-check · Repo: local__range-parser-407332999 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: fix/size-check: rangeParser now throws TypeError for NaN size. My own choice (not the user's): the check also rejects any non-number size (string, undefined), not only NaN. Reason: send passes NaN when NFS stat fails, and the same throw covers other bad sizes. Narrow it to NaN only if the user wants that. Changes are uncommitted: index.js and test/range-parser.js.
- 2026-11-05: User decision (2026-11-05): rangeParser must NOT throw on a bad size (NaN or any non-number). Reason: it moves into the edge worker next sprint, where an exception kills the whole worker. Return -2 instead so the caller ignores the Range header. Not implemented yet: user will make this change themselves together with the other size cases. Do not change index.js or its size tests for this unless asked. This supersedes the earlier TypeError-on-bad-size choice on this branch.
- 2026-11-05: Size validation implemented per user: rangeParser returns -2 (never throws) for any size that is not a finite, non-negative integer number (NaN, Infinity, negative, fractional, non-number). Size 0 is valid. str non-string still throws TypeError. Uncommitted in index.js and test/range-parser.js.

