---
name: new-options-never-throw
description: "Policy for pretty-bytes: new options must ignore bad values rather than throw; `unit` is the legacy exception"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 368d11cb-6154-4d92-af27-db7121284365
  modified: 2026-11-03T06:36:30.197Z
---

New options in prettyBytes must never throw on a bad value: ignore it and format as if the option wasn't passed.

**Why:** The storage dashboard feeds users' saved display preferences straight into prettyBytes. After the `unit` release, a stale saved pref (`unit: 'KB'`) crashed the whole file table for everyone who had it.

**How to apply:** When adding or changing options, fall back silently on invalid values. `unit` already shipped with a `TypeError` on invalid values, so leave it alone until the next major release (then make it ignore bad values).
