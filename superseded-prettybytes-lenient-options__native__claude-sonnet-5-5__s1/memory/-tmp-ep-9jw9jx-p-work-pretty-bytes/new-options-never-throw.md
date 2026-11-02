---
name: new-options-never-throw
description: "Policy for pretty-bytes options: new options must ignore bad values, never throw; `unit` still throws until next major"
metadata:
  node_type: memory
  type: project
  originSessionId: 234871b2-ba1e-4497-b167-7bba3a6c1520
  modified: 2026-11-02T22:14:15.888Z
---

New options added to prettyBytes must never throw on a bad value: ignore it and format as if the option wasn't passed.

**Why:** The storage dashboard feeds users' saved display prefs straight into prettyBytes. After the `unit` release, a stale saved `unit: 'KB'` crashed the whole file table for everyone with it.

**How to apply:** Apply to every new option. `unit` already shipped throwing a TypeError, so leave it alone until the next major. The fraction-digit options (`minimumFractionDigits`/`maximumFractionDigits`) also throw; flagged as candidates to change in the next major.
