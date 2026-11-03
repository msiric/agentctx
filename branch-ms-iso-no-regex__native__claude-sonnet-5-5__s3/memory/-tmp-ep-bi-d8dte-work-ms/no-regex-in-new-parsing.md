---
name: no-regex-in-new-parsing
description: Security reviewer requires hand-written (no regex) parsing code for new code on feat/iso-duration branch
metadata:
  node_type: memory
  type: project
  originSessionId: 9c463ee4-20e3-4648-a0e3-7819724629c0
  modified: 2026-11-03T08:45:32.922Z
---

Leo from security is reviewing the feat/iso-duration PR. Because of the old ReDoS advisory against ms, no regular expressions are allowed in any new parsing code on this branch (ISO 8601 duration parse side must be hand-written).

**Why:** ReDoS advisory history; reviewer requirement.
**How to apply:** When implementing the ISO duration parser, use manual character scanning, not regex. Existing `parse()` regex is untouched.
