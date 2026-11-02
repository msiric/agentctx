---
name: issameorigin-default-ports
description: Decision for the unimplemented isSameOrigin: default ports (:443 https/wss, :80 http/ws) must count as same origin
metadata:
  type: project
---

When implementing `isSameOrigin` (branch feat/same-origin), `https://example.com` and `https://example.com:443` must match, likewise `http://example.com` and `:80`.

**Why:** The company CDN rewrites links with an explicit `:443`; the strict port rule would break them (per platform team).

**How to apply:** `test/same-origin.test.ts` currently has "!=" cases for these (e.g. `https://example.com` != `https://example.com:443`, `http://example.com` != `http://example.com:80`, `wss://example.com` != `wss://example.com:443`) that contradict this and must be flipped when implementing. The user said not to touch those tests until implementation time. Non-default mismatches (`http://example.com:443`, `https://example.com:80`) should still differ.
