---
name: no-positional-booleans
description: User never wants positional boolean parameters in APIs; use options objects
metadata:
  node_type: memory
  type: feedback
  originSessionId: 02bef264-e530-4122-a010-20585fc1cf15
  modified: 2026-11-03T20:07:43.601Z
---

Never use positional boolean parameters in any code written for this user; use a named options object instead (e.g. `parse(str, { requireUnit: true })`, not `parse(str, true)`).

**Why:** `parse(x, true)` tells you nothing at the call site.

**How to apply:** When adding flags to functions/APIs, put them in an options object with a descriptive key.
