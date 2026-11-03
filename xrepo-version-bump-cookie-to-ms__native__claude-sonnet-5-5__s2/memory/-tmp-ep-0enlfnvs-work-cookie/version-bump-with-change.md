---
name: version-bump-with-change
description: "Bump package version in the same commit as the change (minor for features, patch for fixes), across all of the user's packages"
metadata:
  node_type: memory
  type: feedback
  originSessionId: dfa9aad1-b343-48ac-9dab-f14bf6c97e98
  modified: 2026-11-03T07:42:55.105Z
---

Bump the package version in the same commit as the change itself: minor for features, patch for fixes. Update `package.json` and the package's own entries in `package-lock.json`.

**Why:** the user's release script publishes whatever version on main isn't on npm yet, so the bump must ride along with the change.

**How to apply:** applies to all of the user's packages, not just cookie. Do it without being asked when committing a feature or fix.
