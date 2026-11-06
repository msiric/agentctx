# Private notes: local__regexparam-4185223074

- 2026-11-06: npm test is broken on Node 24 (uvu -r esm fails with 'Cannot use import statement outside a module'), and this predates our changes. To run tests, copy src and test to a temp dir as .mjs with a type:module package.json and run npx uvu there. The repo's test setup was left unchanged.
