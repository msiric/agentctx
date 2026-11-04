# feat/same-origin

Branch: feat/same-origin · Repo: local__ufo-3630911018 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: isSameOrigin: user decided ports are compared strictly as written, no default-port normalization (https://a.com !== https://a.com:443). Tests in test/same-origin.test.ts written; implementation deferred.
- 2026-11-04: 2026-11-04: isSameOrigin: REVERSES earlier decision. Default ports now count as same origin (https://a.com === https://a.com:443, http :80 likewise) because the CDN rewrites links with explicit :443 (platform team). test/same-origin.test.ts still encodes the old strict-port rule and must be updated when isSameOrigin is implemented; user said not to touch it for now.
- 2026-11-04: isSameOrigin implemented in src/utils.ts (native URL, default ports normalized, backslash/opaque/relative -> false). 4 port cases in test/same-origin.test.ts fail on purpose until the test file is updated to the default-port rule; user said not to touch it yet.

