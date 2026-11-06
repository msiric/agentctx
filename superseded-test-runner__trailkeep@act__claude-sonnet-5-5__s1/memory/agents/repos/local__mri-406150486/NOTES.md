# Private notes: local__mri-406150486

- 2026-11-06: Use pnpm, not npm, for installs in mri: repo has pnpm-lock.yaml and node_modules is pnpm-layout; 'npm i' crashes with 'Cannot read properties of null'.
- 2026-11-06: mri is migrating tests from tape+tap-spec to uvu (user's choice: matches their other packages; fewer deps). uvu tests use require('uvu') + 'uvu/assert' (CommonJS), end with test.run().
- 2026-11-06: Do not add new devDependencies to this published package (security review blocks them); prefer Node built-ins such as node:test.
