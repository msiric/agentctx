# fork

Branch: fork · Repo: local__mri-3257490167 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: mri '--' option is implemented in src/index.js with tests in test/dashdash.js. My choice (not the user's): with opts['--'] set, argv['--'] is always an array, [] if no bare --, to match minimist. Readme and index.d.ts were deliberately not updated, per the repo rule about upstream files.

