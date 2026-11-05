# Private notes: local__mri-2992804062

- 2026-11-05: This is a fork rebased weekly onto upstream (lukeed/mri). Only src/index.js may be patched among upstream files. Put anything else of ours in NEW files (e.g. new tests in their own test file, fork-ci.yml workflow); never edit readme, types, package.json, ci.yml or other upstream files, to avoid rebase conflicts.
