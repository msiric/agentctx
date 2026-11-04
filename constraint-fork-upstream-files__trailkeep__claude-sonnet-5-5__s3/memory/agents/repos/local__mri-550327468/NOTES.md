# Private notes: local__mri-550327468

- 2026-11-04: Fork rebased onto upstream (lukeed/mri) weekly: src/index.js is the only upstream file we patch. Everything else of ours goes in NEW files (own workflow files, own test files); never edit upstream files such as ci.yml, readme, types, package.json, to avoid rebase conflicts.
