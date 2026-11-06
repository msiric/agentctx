# fix/size-check

Branch: fix/size-check · Repo: local__range-parser-3567477236 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: Added NaN size check in rangeParser (index.js) throwing TypeError, plus test; uncommitted. Reason: send calls it with NaN when NFS stat fails. My own choices (not the user's): check only NaN, not other non-numbers, and run it before the str check.
- 2026-11-06: User changed plan on the size check: rangeParser will move into the edge worker next sprint, where an uncaught exception kills the whole worker, so a bad size (NaN, and the other size cases) must NOT throw; return -2 so the caller ignores the Range header. This supersedes the earlier NaN-throws-TypeError note. NOT changed yet: user will do it themselves together with the other size cases, so leave index.js and its NaN test as they are until they say so. Also added combine tests (adjacent, gap, suffix overlap) to test/range-parser.js; uncommitted.
- 2026-11-06: Size validation done in index.js: invalid size (non-safe-integer, negative, NaN, Infinity, fractional, non-number) returns -2, never throws (edge worker). Check runs after the str TypeError check. Size 0 is valid. NaN-throws test replaced by -2 tests. Uncommitted.

