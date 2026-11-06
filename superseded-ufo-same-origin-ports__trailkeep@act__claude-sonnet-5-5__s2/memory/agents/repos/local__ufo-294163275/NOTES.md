# Private notes: local__ufo-294163275

- 2026-11-06: ufo isSameOrigin: user's rule — compare ports strictly, NO default-port normalization (https://x vs https://x:443 are different origins). Don't add port normalization anywhere in this helper.
- 2026-11-06: ufo isSameOrigin: SUPERSEDES the 2026-11-06 strict-port rule. User's rule now: default ports count as the same origin (https://x == https://x:443, http://x == http://x:80). Reason: the CDN rewrites links with an explicit :443, so strict ports would break them (platform team). Default-port normalization is wanted in this helper.
