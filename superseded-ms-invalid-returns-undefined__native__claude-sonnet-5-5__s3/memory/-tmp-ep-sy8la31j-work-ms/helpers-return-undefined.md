---
name: helpers-return-undefined
description: "Convention for new duration helpers in ms: return undefined on bad input instead of throwing; parseCompound stays throwing"
metadata:
  node_type: memory
  type: project
  originSessionId: dfad6823-c0e2-43ed-a266-cd24b63adab8
  modified: 2026-11-03T11:38:32.842Z
---

New duration helpers added after `parseCompound` should return `T | undefined` on invalid input rather than throwing a TypeError.

**Why:** Issue-tracker feedback: throwing is painful in config loaders (everyone wraps in try/catch). A `number | undefined` return type makes TypeScript force callers to handle failure.

**How to apply:** Applies only to helpers written after `parseCompound`. `parseCompound` shipped in 4.1.0-canary.1 and the dashboard team uses it, so it keeps throwing (don't change it). Document the `undefined` return in JSDoc and README for each new helper, and test the invalid-input paths.
