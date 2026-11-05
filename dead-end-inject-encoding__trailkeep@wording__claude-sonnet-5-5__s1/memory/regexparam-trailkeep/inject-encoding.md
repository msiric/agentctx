# inject-encoding

Branch: inject-encoding · Repo: local__regexparam-3008468904 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: Open question from user: whether URI-encoding of inject() values belongs in regexparam or in their uploader client; user said hold off on encoding. Finding: plain encodeURIComponent does NOT match the storage service's signed path (leaves ! ' ( ) * raw); this wrapper does: encodeURIComponent(s).replace(/[!'()*]/g, c => '%'+c.charCodeAt(0).toString(16).toUpperCase()). Unverified: service's handling of '*'. Do not change inject() encoding until the user decides.
- 2026-11-05: Fixed inject() treating numeric 0 as missing (src/index.js: (x || x === 0)); added two tests in test/inject.js. Uncommitted; tests not run via uvu (runner broken), only checked manually. ''/null/false still count as missing - my choice, minimal change.
- 2026-11-05: User lifted the hold and asked for inject() percent-encoding in regexparam. Implemented in src/index.js: encodeURIComponent plus %-encoding of ! ' ( ) * (matches the storage service's signed path; plain encodeURIComponent does not). Wildcard '*' values are split on '/', each segment encoded, slashes kept. Added 5 tests in test/inject.js. Uncommitted. uvu runner still broken (esm loader), so only checked via a temp .mjs copy; new tests not run. Still unverified: how the service handles '*' encoded as %2A.

