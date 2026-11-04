# feat/same-origin

Branch: feat/same-origin · Repo: local__ufo-678101157 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: isSameOrigin: strict port comparison, no default-port normalization (https://x and https://x:443 are NOT same origin) - user decision, doesn't want magic port normalization
- 2026-11-04: isSameOrigin: REVERSES the 2026-11-04 strict-port decision. Default ports now count as same origin (https://x == https://x:443, http://x == http://x:80) because the CDN rewrites links with an explicit :443 (platform team). Same-origin tests in test/same-origin.test.ts deliberately left untouched until isSameOrigin is implemented.

