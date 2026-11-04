# feat/same-origin

Branch: feat/same-origin · Repo: local__ufo-1944193608 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: isSameOrigin: ports are compared strictly, no default-port normalization (https://x vs https://x:443 are NOT same origin). User decision; tests in test/same-origin.test.ts, implementation still pending.
- 2026-11-04: isSameOrigin DECISION CHANGE (supersedes strict-port entry): default ports are normalized, so https://x and https://x:443 ARE same origin, same for http :80. Reason: platform team says our CDN rewrites links with explicit :443, strict rule would break it. test/same-origin.test.ts still encodes the old strict rule and must be updated when isSameOrigin is implemented (user said not to touch it yet).
- 2026-11-04: isSameOrigin implemented in src/utils.ts (default-port normalization, only http/https/ws/wss; protocol-relative only matches protocol-relative). test/same-origin.test.ts updated to the normalized-port rule.

