# feat/same-origin

Branch: feat/same-origin · Repo: local__ufo-2085792720 · Kind: branch · Created: 2026-11-02

## Goal

Add an `isSameOrigin(a, b)` helper to ufo. Tests first, to agree on semantics; implementation comes in a later session.

## Done when

- `isSameOrigin` is implemented in `src/utils.ts` and exported from `src`.
- `test/same-origin.test.ts` passes, with the `@ts-expect-error` on its import removed.
- The rest of the test suite still passes.

## Plan

- [x] Write test cases in `test/same-origin.test.ts` (not run yet)
- [x] Implement `isSameOrigin` in `src/utils.ts` and export it
- [x] Remove the `@ts-expect-error` from the test import
- [x] Run the full test suite

## Progress

2026-11-02: wrote test/same-origin.test.ts (not run, no implementation). Next: implement isSameOrigin, export it, drop the @ts-expect-error, run tests.
2026-11-02: unrelated joinURL fix (query/hash kept at end) done on this branch, in src/utils.ts and test/join.test.ts. Port semantics changed to default-port normalization (see Decisions); same-origin tests not yet updated, to be done at implementation time.
2026-11-02: implemented isSameOrigin in src/utils.ts (exported via utils), updated tests to default-port normalization, removed @ts-expect-error. Full suite (529) and tsc pass. Trailing-dot hosts still open.

## Decisions and dead ends

- Default ports normalize (2026-11-02, supersedes the earlier strict-ports rule): `https://x` and `https://x:443` are the same origin, likewise `http://x` and `http://x:80`. Reason: the CDN rewrites links with an explicit :443 (platform team). Non-default ports still must match. `new URL().origin` strips default ports, so it can be used for this.
- The existing tests in `test/same-origin.test.ts` still encode the old strict-ports rule. Deliberately not updated yet (user's call); fix them when implementing.
- Scheme and host are case-insensitive; userinfo, path, query and hash are ignored.
- IDN host equals its punycode form.
- Opaque origins (`data:`, `javascript:`, `mailto:`, `tel:`) are never same-origin, not even with themselves.
- Relative vs relative is true; relative vs absolute is false.
- Protocol-relative (`//host`) only matches another protocol-relative URL with the same host.
- Malformed absolute URLs return false without throwing.

## Open questions

- Trailing-dot hosts (`example.com.`): semantics unclear, no test case yet.
