# test-runner

Branch: test-runner · Repo: local__mri-2713141908 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: Test migration on this branch uses node:test (not uvu). Leave test/num.js as is for now; it gets redone with the rest of the tests.
- 2026-11-04: Test migration finished on node:test (all 3 files in test/ converted); tape, tap-spec and uvu removed from devDependencies. Test script: node --test test/*.js.

