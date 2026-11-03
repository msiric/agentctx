# HANDOFF

## State
Task: add `isSameOrigin(a, b)` helper to ufo (branch `feat/same-origin`).
- DONE: implemented in `src/utils.ts` (via `new URL(x).origin`; "null"/throw/empty -> false). Exported through `src/index.ts` (`export * from ./utils`).
- Tests in `test/same-origin.test.ts` updated to the revised default-port rule; `@ts-expect-error` removed.
- Full suite passes (523), `tsc --noEmit` clean. Nothing committed yet.

## Decisions (proposed, awaiting user agreement)
- Origin = protocol + hostname + port; path/query/hash/credentials ignored.
- Protocol and host case-insensitive; punycode equals unicode host.
- Ports: REVISED by user (platform team: CDN rewrites links with explicit :443). Default ports now count as the same origin: `https://example.com` == `https://example.com:443`, `http://example.com` == `http://example.com:80`. Non-default ports must match exactly; `http://example.com:443` != `http://example.com` (443 is not http's default). `URL.origin` normalizes default ports, so it is usable now. (Previous decision was strict ports; superseded.)
- Tests were updated to the default-port rule when implementing (previously stale).
- Trailing-dot host is treated as different (matches WHATWG `URL.origin`).
- Relative, protocol-relative, empty, malformed, and opaque-origin (data:, javascript:, mailto:) inputs return `false` and never throw. Reason: no origin means nothing to be "same" with, and a security-oriented check should fail closed.
- Style follows `test/is-same.test.ts` (table-driven, symmetric checks).

## Open questions
- Should two identical relative paths be "same origin"? Tests currently say false.
- Should `//example.com` be resolved against a base? Currently false.

## Failed approaches
None yet.

## Side task: joinURL query/hash fix (done, same branch, uncommitted)
- `joinURL` (src/utils.ts) now splits the accumulated URL at the first `?`/`#`, appends the segment to the path part, and re-attaches the suffix: `joinURL("/api?v=2", "users")` -> `/api/users?v=2`.
- Tests: `joinURLQueryHashTests` in test/join.test.ts (kept joinURL-only; putting them in the shared `joinURLTests` list also runs them against `joinRelativeURL`, which has the same bug and was NOT changed, since only joinURL was requested).
- Known limit: a later segment that itself contains `?`/`#` is not merged with the base's query (e.g. `joinURL("/a?x=1", "b?y=2")` yields `/a/b?y=2?x=1`... untested/undefined behavior).
- This is unrelated to the isSameOrigin work; consider a separate commit.
