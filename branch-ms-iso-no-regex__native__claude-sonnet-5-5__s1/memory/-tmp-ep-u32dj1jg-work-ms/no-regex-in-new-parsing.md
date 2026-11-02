---
name: no-regex-in-new-parsing
description: Security reviewer requires hand-written (no regex) parsing code for new work on feat/iso-duration
metadata:
  node_type: memory
  type: project
  originSessionId: aad306a6-d881-451e-8fd1-3ad12b942318
  modified: 2026-11-02T18:29:07.312Z
---

Leo (security) is reviewing the feat/iso-duration PR and wants no regular expressions in any new parsing code on this branch, due to the old ReDoS advisory against ms.

**Why:** prior ReDoS advisory against ms.
**How to apply:** when implementing ISO 8601 duration parsing (the next step after `formatISO`), write a hand-rolled character scanner, not regex.
