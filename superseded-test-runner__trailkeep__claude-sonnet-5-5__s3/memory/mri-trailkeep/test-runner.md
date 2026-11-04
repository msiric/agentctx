# test-runner

Branch: test-runner · Repo: local__mri-4157336578 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: Test migration to node:test done (tape/tap-spec/uvu removed, test script is 'node --test test/'). Open: test 'explicit empty value (--foo=)' in test/index.js fails because lib doesn't yield foo:'' for '--foo=' - decide whether to fix lib or drop the test. Nothing committed yet.

