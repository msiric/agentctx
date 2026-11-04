# Private notes: local__regexparam-2418638733

- 2026-11-04: npm test (uvu -r esm) fails on this Node version with 'Cannot use import statement outside a module', before any change. Workaround: copy src, test and package.json to a temp dir, add "type":"module", point imports at ../src/index.js, run npx uvu test.
