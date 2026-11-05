# feat/same-origin

Branch: feat/same-origin · Repo: local__ufo-1211467820 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: isSameOrigin: ports are compared strictly, no default-port normalization (user's rule: 'I don't want magic port normalization'). https://example.com and https://example.com:443 must NOT be same-origin; tests in test/same-origin.test.ts cover it. Implementation not written yet; do it next.
- 2026-11-05: isSameOrigin: user reviewed the PROPOSED semantics in test/same-origin.test.ts and said 'looks reasonable' (relative/protocol-relative/opaque protocols -> false, credentials ignored, IDN==punycode), only overriding ports. The test cases were my proposals, so re-check the IDN/punycode case against strict-port philosophy when implementing.
- 2026-11-05: isSameOrigin: SUPERSEDES the earlier strict-port rule. User now wants default-port normalization (https://example.com == https://example.com:443, http :80 likewise) because the CDN rewrites links with explicit :443 (platform team). Non-default ports still compared strictly. test/same-origin.test.ts still encodes the OLD strict rule (cases like 'https://example.com !== https://example.com:443', ':80' ones, and 'http://example.com:443 !== http://example.com' stay different) and must be updated when implementing; user said not to touch those tests yet. Also re-check IDN==punycode case when implementing. Unrelated: joinURL query/hash fix done in src/utils.ts + test/join.test.ts; joinRelativeURL still has the same bug (not requested).
- 2026-11-05: isSameOrigin implemented in src/utils.ts (native URL origin compare; default-port normalization; relative/protocol-relative/opaque/invalid -> false). Not yet exported-checked beyond tests. test/same-origin.test.ts still has 3 old strict-port cases failing (https :443, http :80, https :443 with paths) - user said not to touch tests yet; ask before moving them to the same-origin list and updating the header comment. IDN==punycode confirmed passing.

