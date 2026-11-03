# feat/same-origin

Branch: feat/same-origin · Repo: local__ufo-2422072516 · Kind: branch · Created: 2026-11-03

## Decisions and dead ends

- 2026-11-03: isSameOrigin: ports compared strictly, no default-port normalization (https://x.com != https://x.com:443); user doesn't want magic port normalization. Tests in test/same-origin.test.ts, implementation still pending.
- 2026-11-03: isSameOrigin: REVERSES earlier decision. Default ports now normalize (https://x.com == https://x.com:443, http :80 likewise) because the CDN rewrites links with explicit :443 (per platform team). test/same-origin.test.ts still encodes the old strict-port rule and must be updated when isSameOrigin is implemented; user said not to touch it yet.

