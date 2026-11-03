---
name: same-origin-default-ports
description: "Decision for isSameOrigin: default ports (:443 https, :80 http) must count as same origin as the portless URL"
metadata:
  node_type: memory
  type: project
  originSessionId: feb18db9-4542-41cc-a27d-a437dbd34063
  modified: 2026-11-03T06:43:29.874Z
---

`isSameOrigin` (branch feat/same-origin, not yet implemented) must treat default ports as equal: `https://example.com` matches `https://example.com:443`, and `http://x` matches `http://x:80`.

**Why:** The user's CDN rewrites links with an explicit `:443`, so a strict port comparison would break them (decided with the platform team).

**How to apply:** When implementing `isSameOrigin`, normalize default ports before comparing. The existing untracked `test/same-origin.test.ts` may assert the old strict-port rule. Update those tests then, but only when implementing, because the user said not to touch them for now.
