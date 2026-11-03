# HANDOFF

## Task
Add `isSameOrigin(a, b)` to ufo.

## State
- IMPLEMENTED in `src/utils.ts` (uses native `URL`; `origin` handles default-port normalization, punycode, case). Exported via index.
- `test/same-origin.test.ts` updated to the revised port rule (default ports now in the same-origin list; `http://example.com:443` != `http://example.com` kept). Full suite, tsc, eslint pass.
- Not committed.

## Remaining open questions for user
- ws:80 / wss:443 normalize too (assumed, WHATWG defaults; tests encode it).
- relative-vs-relative `true`, `//host` vs absolute `false` accepted with "looks reasonable".
- Added (not discussed): two protocol-relative URLs compare by host (`//a.com` == `//a.com/x`); relative vs `//host` false.

## Semantic decisions (open for user review)
- Origin = protocol + host + port; path/query/hash/credentials ignored.
- Protocol/host case-insensitive; unicode host == punycode.
- Ports (REVISED, user decision after talking to platform team): default ports DO normalize. `https://example.com` == `https://example.com:443`, `http://example.com` == `http://example.com:80`. Reason: our CDN rewrites links with an explicit :443, so strict matching would break us. Non-default explicit ports still must match exactly (`https://example.com:8443` != `https://example.com`; `http://example.com:443` != `http://example.com`).
  - Open question: user only named https:443 and http:80. Assumption to confirm: ws:80 / wss:443 normalize too (same rule, WHATWG URL defaults).
  - SUPERSEDED: earlier strict rule; tests were flipped when implementing.
- Both relative -> true; relative vs absolute -> false; protocol-relative `//host` vs absolute -> false.
- Opaque origins (data:, javascript:, mailto:) -> never same-origin, even to themselves.
- Empty strings -> true (both relative); `"http://"` -> false, no throw.
- Always symmetric.

## Failed approaches
None yet.

## Side task (done): joinURL query/hash
- `joinURL("/api?v=2", "users")` now -> `/api/users?v=2` (src/utils.ts joinURL; tests in test/join.test.ts `joinURLQueryTests`).
- Decision: base's `?`/`#` suffix is moved to the end only when the appended segment has no `?`/`#` of its own; otherwise legacy behavior (ambiguous case).
- `joinRelativeURL` has its own implementation and was NOT changed (out of scope), so the new cases are in a joinURL-only list, not the shared one.
- Full suite: only the expected unimplemented `same-origin` tests fail.
