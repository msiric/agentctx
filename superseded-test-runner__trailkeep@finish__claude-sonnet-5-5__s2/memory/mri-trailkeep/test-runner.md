# test-runner

Branch: test-runner · Repo: local__mri-769497670 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: Migrating tests from tape/tap-spec to uvu (matches user's other packages), one file at a time. test/num.js done; index.js and unknown.js still tape. 'test' script lists tape files explicitly because the old test/*.js glob would load uvu files under tape; move each converted file to the uvu side, finish with 'uvu test' and drop tape + tap-spec. Repo uses pnpm (npm install fails on node_modules).
- 2026-11-04: Test migration target changed from uvu to node:test. Reason: security review blocks adding new devDependencies to published packages. Supersedes the uvu decision. test/num.js is already uvu; leave it as is for now, user will redo it with the remaining files. Don't add uvu to other files.
- 2026-11-04: Test migration finished: index.js, unknown.js, num.js all on node:test + node:assert/strict; tape, tap-spec, uvu removed from package.json; 'test' script is 'node --test test/*.js'. 24 tests pass. Supersedes the 'leave num.js as uvu' note.

