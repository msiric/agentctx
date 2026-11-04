# test-runner

Branch: test-runner · Repo: local__mri-2471915271 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: Test migration uses Node's built-in node:test, not uvu: security review blocks new devDependencies in published packages. Leave test/num.js untouched until the rest is migrated.

