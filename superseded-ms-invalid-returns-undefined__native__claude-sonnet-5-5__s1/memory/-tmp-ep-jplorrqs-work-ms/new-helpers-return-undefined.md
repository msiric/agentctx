---
name: new-helpers-return-undefined
description: "Convention for new parse-style helpers in ms: return undefined on bad input instead of throwing; parseCompound stays throwing"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 5795ae40-e9c6-4e0c-9611-294530b269de
  modified: 2026-11-02T21:51:09.483Z
---

New parsing/duration helpers added after `parseCompound` should return `number | undefined` (i.e. `undefined` on bad input) rather than throwing a `TypeError`.

**Why:** Issue-tracker feedback: throwing is painful in config loaders, where everyone wraps calls in try/catch. A `number | undefined` return type makes TypeScript force callers to handle failure.

**How to apply:** Don't change `parseCompound` (published in 4.1.0-canary.1, dashboard team uses it; it keeps throwing). Apply the undefined-on-failure convention only to later helpers, and document it in the README and JSDoc. Existing `parse` behavior is unchanged. See [[parse-compound-published]].
