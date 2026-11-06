# feat/same-origin

Branch: feat/same-origin · Repo: local__ufo-294163275 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: ufo isSameOrigin(a,b): tests written first in test/same-origin.test.ts (no impl yet, by user request). Semantics in the test header are MY proposal pending user agreement (relative/protocol-relative/opaque origins => false, default ports normalized, userinfo ignored).
- 2026-11-06: isSameOrigin: tests agreed with user (strict ports covered). Next: implement in src, not started.
- 2026-11-06: isSameOrigin: port semantics changed to default-port normalization (see repo note); the strict-port cases in test/same-origin.test.ts are now outdated. User said NOT to touch those tests yet (pushing branch for the joinURL fix); revisit/update them when implementing isSameOrigin. Also: joinURL query/hash fix done (uncommitted at time of note); joinRelativeURL still has the same query-order bug, left alone.
- 2026-11-06: isSameOrigin implemented in src/utils.ts (native URL, network schemes only, default ports normalized); strict-port tests updated to match. My choice: blob:/file:/data: => false via protocol allowlist (http/https/ws/wss/ftp).

