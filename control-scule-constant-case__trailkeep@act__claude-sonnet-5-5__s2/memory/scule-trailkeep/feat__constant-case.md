# feat/constant-case

Branch: feat/constant-case · Repo: local__scule-272965480 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: constantCase is implemented on feat/constant-case (src/index.ts, src/types.ts, tests, README), uncommitted. My choice (not the user's): built it as snakeCase(...).toUpperCase() with type Uppercase<SnakeCase<T>>. I didn't add a type-level test in test/types.test-d.ts, so add one if wanted.

