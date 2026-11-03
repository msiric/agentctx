---
name: issameorigin-default-ports
description: "Decision for isSameOrigin: default ports (:443 https, :80 http) count as same origin as the portless URL"
metadata:
  node_type: memory
  type: project
  originSessionId: 1a53ea6c-a10a-4a9f-833e-80bf12fdd90e
  modified: 2026-11-03T13:23:41.979Z
---

`isSameOrigin` must treat explicit default ports as equal to no port: `https://example.com` ~ `https://example.com:443`, and `http://example.com` ~ `http://example.com:80`. Non-default ports (e.g. :8443, `https://...:80`, `http://...:443`) still differ.

**Why:** Platform team said the CDN rewrites links with an explicit `:443`, so the strict port rule would break them.

**How to apply:** Implemented 2026-11-03 via `new URL().origin` in `src/utils.ts`; the three strict-port tests in `test/same-origin.test.ts` were flipped to same-origin. Keep default-port normalization if the function is touched again.
