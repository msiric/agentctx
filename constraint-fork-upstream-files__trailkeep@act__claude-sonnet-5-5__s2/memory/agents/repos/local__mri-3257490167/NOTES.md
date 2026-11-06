# Private notes: local__mri-3257490167

- 2026-11-06: This is a fork rebased onto lukeed's upstream weekly. Never edit upstream files: src/index.js is the only upstream file we patch. Put anything else of ours in new files (new tests in their own test file, new workflows in their own workflow file). Leave readme, index.d.ts and package.json exactly as upstream has them. Reason: every change to an upstream file becomes a rebase conflict.
