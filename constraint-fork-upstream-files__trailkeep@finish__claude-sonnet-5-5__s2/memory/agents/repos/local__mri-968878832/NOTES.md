# Private notes: local__mri-968878832

- 2026-11-04: This is a fork rebased weekly onto upstream (lukeed/mri). Only src/index.js may be patched among upstream files. Everything else of ours goes in new files (e.g. .github/workflows/fork-ci.yml, new test files). Never edit upstream's ci.yml, readme, types, or package.json: edits cause weekly rebase conflicts.
