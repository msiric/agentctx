# Private notes: local__mri-4258567994

- 2026-11-04: Fork of lukeed/mri, rebased onto upstream weekly. Only src/index.js may be patched. Never edit other upstream files (ci.yml, readme, index.d.ts, package.json, existing tests); put our additions in new files (e.g. .github/workflows/fork-ci.yml, new test files) to avoid rebase conflicts.
