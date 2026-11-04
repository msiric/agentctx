# Private notes: local__mri-2790632037

- 2026-11-04: Fork rebased weekly onto lukeed/mri upstream. Only src/index.js may be patched; never edit other upstream files (ci.yml, readme, types, package.json, existing tests). Put our additions in new files (own workflow files, own test files) to avoid rebase conflicts.
