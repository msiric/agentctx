---
name: new-options-never-throw
description: "Policy for pretty-bytes options: new options must ignore bad values rather than throw; `unit` still throws until next major"
metadata:
  node_type: memory
  type: feedback
  originSessionId: e03259e4-448a-4fcb-be20-22dca68b7806
  modified: 2026-11-03T12:35:52.396Z
---

New options added to prettyBytes must never throw on a bad value. Ignore the value and format as if the option wasn't passed.

**Why:** The storage dashboard feeds users' saved display preferences straight into prettyBytes. After the `unit` release (7.2.x), a stale saved pref (`unit: 'KB'`) threw a TypeError and crashed the whole file table for everyone with it.

**How to apply:** When adding or changing options, fall back silently on invalid input and document that in the readme. The exception is `unit`, which has already shipped with the throw: leave it alone until the next major, then change it to ignore bad values too (and update the readme line saying it throws a `TypeError`).
