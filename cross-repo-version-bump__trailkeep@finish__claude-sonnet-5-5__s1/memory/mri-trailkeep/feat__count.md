# feat/count

Branch: feat/count · Repo: local__mri-1134686782 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: opts.count: count keys are also treated as booleans (never consume next arg); --no-<key> resets to 0 not false (author's call, unconfirmed by user); absent keys stay undefined unless defaulted. Bumped to 1.3.0 (minor, new feature). Changes uncommitted.

