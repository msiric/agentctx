---
name: no-positional-boolean-params
description: User never wants positional boolean parameters in APIs; use an options object instead
metadata:
  node_type: memory
  type: feedback
  originSessionId: ae780ecc-ca0b-48e7-a307-ba8b7ab60652
  modified: 2026-11-04T00:57:37.061Z
---

Never add positional boolean parameters to functions. Use a named options object (e.g. `parse(str, { requireUnit: true })`), not `parse(str, true)`.

**Why:** a bare boolean at the call site tells the reader nothing about what it does.

**How to apply:** whenever adding a flag or toggle to a function signature in this or any of the user's code, make it a property on an options object.
