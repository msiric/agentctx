# HANDOFF

## Task
Add `isSameOrigin(a, b)` to ufo. Semantics agreed; IMPLEMENTED in `src/utils.ts` (exported via `src/index`). Not committed.

## State
- `isSameOrigin` uses native `new URL(x).origin`; opaque origin ("null"), empty, nullish or throwing input -> false.
- `test/same-origin.test.ts` updated to the default-port decision (stale "strict ports" block flipped, plus a non-default-port test). Full suite passes (534 tests).

## Decisions (user said "looks reasonable" to the proposal, with the port change below)
- Origin = scheme + host + port (WHATWG). Path, query, hash and userinfo are ignored.
- SUPERSEDED (user, after talking to the platform team: the CDN rewrites links with an explicit `:443`): default ports now DO count as the same origin. `https://example.com` matches `https://example.com:443`; `http://example.com` matches `http://example.com:80`. This replaces the earlier "strict ports, no normalization" decision.
  - Tests were updated to match when implementing.
  - Implementation note: a plain WHATWG URL parse already normalizes default ports (`new URL("https://example.com:443").port === ""`), so no special port handling is needed. A non-default port (e.g. `:8443`) must still differ.
- Scheme and host are case-insensitive. IDN hosts match their punycode form.
- Relative, protocol-relative, empty and opaque-origin inputs (data:, mailto:, javascript:, file:) always return false, even when compared with themselves. Reason: they have no usable origin and a security helper should fail closed.
- Nullish or malformed input returns false and does not throw.
- Accepts strings or URL objects.
- Trailing-dot hosts are treated as distinct origins (matches WHATWG).

## Open questions (implemented per the proposals; revisit if user disagrees)
- Identical relative paths: not same-origin.
- `file:` URLs: not same-origin.

## Side task (done): joinURL query/hash fix
- `joinURL` in `src/utils.ts` now splits the accumulated URL at the first `?`/`#`, joins the segment onto the path, then re-appends the suffix. `joinURL("/api?v=2", "users")` → `/api/users?v=2`.
- Decision: if a joined segment carries its own `?`/`#`, the segment's suffix wins and the base's is dropped (merging queries seemed out of scope). 
- Tests added in `test/join.test.ts` (separate describe, since `joinRelativeURL` reuses `joinURLTests`). Full suite passes except the intentionally failing `same-origin.test.ts` (excluded from the run). Not committed.

## Failed approaches
None yet.
