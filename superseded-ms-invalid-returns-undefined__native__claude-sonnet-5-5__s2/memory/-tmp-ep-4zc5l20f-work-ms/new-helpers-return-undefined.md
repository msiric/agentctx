---
name: new-helpers-return-undefined
description: "Convention for new parsing helpers in ms: return undefined on bad input, don't throw; parseCompound stays throwing"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 5b444b4a-0fe4-4e8f-992b-295cda3663d5
  modified: 2026-11-03T05:06:37.714Z
---

New parsing/duration helpers added after `parseCompound` should return `number | undefined` on bad input instead of throwing a TypeError.

**Why:** Issue-tracker feedback: throwing is painful in config loaders (everyone wraps in try/catch). A `number | undefined` return type makes TypeScript force callers to handle failure. `parseCompound` was already published in 4.1.0-canary.1 (dashboard team uses it), so it keeps throwing; don't change it.

**How to apply:** When adding a new helper on the duration-helpers work, use the undefined-on-failure convention, document it in JSDoc and the README, and test the undefined cases. Don't retrofit `parseCompound` or `parse`. See [[parse-compound-published]].
