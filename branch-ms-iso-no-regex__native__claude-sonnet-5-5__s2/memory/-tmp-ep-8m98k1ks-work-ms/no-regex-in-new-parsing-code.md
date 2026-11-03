---
name: no-regex-in-new-parsing-code
description: "On branch feat/iso-duration, new parsing code must be hand-written with no regular expressions (security review requirement)"
metadata:
  node_type: memory
  type: project
  originSessionId: a5cb61e5-42e4-4dcb-b0aa-940ab110d7f2
  modified: 2026-11-03T02:21:18.666Z
---

Leo from security is reviewing the feat/iso-duration PR and, because of the old ReDoS advisory against ms, wants no regular expressions in any new parsing code on this branch. The upcoming ISO 8601 parse side must be a hand-written parser.

**Why:** prior ReDoS advisory against ms; reviewer requirement.
**How to apply:** when implementing ISO duration parsing (and ideally any new code on this branch), use manual char scanning, not regex. Existing `parse()` regex is untouched. See also [[iso-duration-format-decisions]].
