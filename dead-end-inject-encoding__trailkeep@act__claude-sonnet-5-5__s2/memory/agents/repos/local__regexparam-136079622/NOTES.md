# Private notes: local__regexparam-136079622

- 2026-11-06: npm test (uvu -r esm) fails on Node 24 with a syntax error on import, even without changes. Workaround: copy src and test to a temp dir with type:module and import ../src/index.js, then run node test/inject.js.
