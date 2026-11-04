# Private notes: local__mri-1262646678

- 2026-11-04: Fork rebases weekly onto upstream (lukeed/mri). Only src/index.js may be edited among upstream files; everything else of ours goes in new files (e.g. .github/workflows/fork-ci.yml, new test files). Never edit readme, types, package.json, ci.yml - avoids rebase conflicts.
