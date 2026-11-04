# feat/same-origin

Branch: feat/same-origin · Repo: local__ufo-1993860612 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: isSameOrigin: strict port comparison, NO default-port normalization (https://x vs https://x:443 are NOT same origin). User doesn't want magic port normalization. Tests in test/same-origin.test.ts; implementation still pending.
- 2026-11-04: REVERSES earlier decision. isSameOrigin SHOULD normalize default ports: https://example.com == https://example.com:443, http :80 likewise. Reason: platform team says our CDN rewrites links with explicit :443, so strict port comparison would break us. test/same-origin.test.ts still encodes the old strict rule (untracked, not yet updated); user said leave it alone for now and fix tests when implementing isSameOrigin. Implementation still pending.
- 2026-11-04: isSameOrigin implemented in src/utils.ts with default-port normalization (http/ws 80, https/wss 443, ftp 21); tests in test/same-origin.test.ts updated to match. Relative/protocol-less/invalid inputs never match. Remaining: README/docs mention if wanted.

