# test-runner

Branch: test-runner · Repo: local__mri-2150818072 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: mri fix: explicit empty value '--foo=' now yields foo:'' and leaves next arg positional (lib/index.js, test in test/index.js). Side effect: toVal no longer turns an empty-string value into 0 (e.g. ['-x',''] gives '' not 0).
- 2026-11-05: Test migration to node:test is DONE (index/num/unknown converted, tape/tap-spec/uvu removed from package.json, script is 'node --test test/'). lib/ is gitignored and rebuilt from src/ by pretest, so fixes must go in src/index.js: re-applied the '--foo=' empty-value fix there (my edit; earlier lib-only edit was lost on rebuild).

