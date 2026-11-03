---
name: version-bump-with-change
description: "Bump package version in the same commit as each change (minor for features, patch for fixes)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: dc9b4270-e7e6-449c-aef5-bd96c266515b
  modified: 2026-11-03T01:46:15.821Z
---

Include the version bump (package.json + package-lock.json) in the same commit as the change itself: minor for features, patch for fixes.

**Why:** The user's release script publishes whatever version on main isn't on npm yet, so the bump must ride along with the change. They want this in all their packages.

**How to apply:** Run `npm version <minor|patch> --no-git-tag-version` before committing a feature/fix.
