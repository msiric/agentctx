# Private notes: local__regexparam-3008468904

- 2026-11-05: npm test (uvu -r esm) fails on this Node version with 'Cannot use import statement outside a module' (esm loader broken), before any change. Verify inject changes by copying src/index.js to a temp .mjs and running it directly until the runner is fixed.
