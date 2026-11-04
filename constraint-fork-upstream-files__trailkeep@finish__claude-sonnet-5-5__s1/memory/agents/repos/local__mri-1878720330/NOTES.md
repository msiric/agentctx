# Private notes: local__mri-1878720330

- 2026-11-04: Fork of lukeed/mri, rebased weekly onto upstream. Only src/index.js may be patched; never edit other upstream files (ci.yml, readme, types, package.json). Our additions go in new files (e.g. .github/workflows/ci-fork.yml, new test files) to avoid rebase conflicts.
