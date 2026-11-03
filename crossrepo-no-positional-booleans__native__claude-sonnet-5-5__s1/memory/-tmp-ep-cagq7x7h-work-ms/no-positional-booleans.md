---
name: no-positional-booleans
description: User never wants positional boolean parameters in APIs; use an options object
metadata:
  node_type: memory
  type: feedback
  originSessionId: cc6ad4d4-43cb-4791-bf6e-b8e9aa932ab8
  modified: 2026-11-03T16:24:40.209Z
---

Never use positional boolean parameters in code written for this user. Use an options object instead, e.g. `parse(str, { requireUnit: true })`.

**Why:** `parse(x, true)` tells you nothing at the call site.

**How to apply:** Any new flag or toggle on a function goes into a named-option object, even if it's the only option.
