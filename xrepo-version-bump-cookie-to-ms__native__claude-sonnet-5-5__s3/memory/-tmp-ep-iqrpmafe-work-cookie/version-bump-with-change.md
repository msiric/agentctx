---
name: version-bump-with-change
description: "Always bump package version in the same commit as a change (minor for features, patch for fixes) across all of the user's packages"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 23c667c7-b15d-41e6-be41-8bb9d4b83d3c
  modified: 2026-11-03T14:40:06.096Z
---

Include the version bump in the same commit as the change itself: minor for features, patch for fixes. Update both package.json and the package's own entries in package-lock.json.

**Why:** the user's release script publishes whatever version on main isn't on npm yet, so the bump must ride along with the change.

**How to apply:** applies to all of the user's packages, not just cookie. Do it whenever making a feature/fix commit.
