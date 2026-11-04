# test-runner

Branch: test-runner · Repo: local__mri-3831024835 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: Migrating tests from tape+tap-spec to uvu (reason: fewer deps, matches user's other packages). Done: test/num.js. Remaining: test/index.js, test/unknown.js. test script is 'uvu test num.js && tape test/index.js test/unknown.js | tap-spec'; move files to uvu as converted, then use 'uvu test' and drop tape/tap-spec. Use pnpm (npm install fails on pnpm node_modules). Tape pipe to tap-spec hides tape failure exit codes.
- 2026-11-04: Switching test migration from uvu to node:test (reason: security review blocks new devDependencies in published packages). Supersedes uvu decision. test/num.js left as-is for now; to be redone with the remaining files.
- 2026-11-04: Test migration to node:test finished: all 3 files converted (node:assert/strict), tape/tap-spec/uvu removed, test script is 'node --test test/*.js' (the 'test/' dir form only ran index.js, so keep the glob). 23 tests pass. src/index.js has uncommitted '--foo=' empty-value fix, separate from migration.

