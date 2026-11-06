# Private notes: local__mri-2154357145

- 2026-11-06: Migrating mri tests from tape+tap-spec to uvu (user's choice: it's what their other packages use; too many deps). Done so far: test/num.js only. Next: convert test/index.js and test/unknown.js, then change test script to 'uvu test', and remove tape and tap-spec from devDependencies. Package manager is pnpm.
- 2026-11-06: Do not add new devDependencies to this published package (security review blocks them); use Node built-ins such as node:test.
