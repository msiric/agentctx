# fork

Branch: fork · Repo: local__mri-2862066392 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: Added opts['--'] support in src/index.js with tests in test/dashes.js. Readme and index.d.ts are NOT updated for it, because the repo rule forbids editing upstream files. Ask the user before touching them. My choice (not the user's): argv['--'] is always [] when opts['--'] is set, matching minimist.

