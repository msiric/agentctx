# Private notes: local__mri-2339343008

- 2026-11-05: Use pnpm, not npm, for installs in mri (pnpm-lock.yaml; npm install errors on the pnpm-managed node_modules).
- 2026-11-05: Security review blocks adding new devDependencies to packages we publish; prefer built-ins (e.g. node:test).
