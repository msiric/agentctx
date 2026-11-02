# Headroom gate, batch 1 (2026-11-02)

The rule is in `PREREGISTRATION.md`. A fact trap is dropped if `none`
passes it in at least 2 of 3 seeds (no headroom), or if `oracle-note` fails
it in at least 2 of 3 (broken). The rule only uses `none` and
`oracle-note`. Model: claude-sonnet-5-5. The raw cells are on the
`bench-results` branch.

| Trap | Split | none | oracle-note | Verdict |
|---|---|---|---|---|
| decision-schedule-reraise | dev (pilot) | 0/3 | 3/3 | keep |
| branch-ms-iso-no-regex | dev | 1/3 | 3/3 | keep |
| crossrepo-table-driven-tests | dev | 0/3 | 3/3 | keep |
| superseded-ms-invalid-returns-undefined | dev | 0/3 | 3/3 | keep |
| superseded-ufo-same-origin-ports | dev | 0/3 | 3/3 | keep |
| constraint-schedule-no-module-shortcuts | held-out | 0/3 | 3/3 | keep |
| crossrepo-no-positional-booleans | held-out | 0/3 | 3/3 | keep |
| deadend-tinydb-mtime-cache | held-out | 1/3 | 3/3 | keep |
| decision-tinydb-yaml-bools | held-out | 0/3 | 3/3 | keep |
| branch-ufo-parse-ts-frozen | dev | 2/3 | 3/3 | drop: no headroom |
| deadend-tinydb-streaming-write | dev (pilot) | 3/3 | 3/3 | drop: no headroom |
| constraint-dotenv-no-values | dev (pilot) | 3/3 | 3/3 | drop: no headroom |
| control-scule-constant-case | dev | 3/3 | 3/3 | control |
| control-dotenv-get-default | held-out | 3/3 | 3/3 | control |

Of 12 fact traps, 9 are kept: 5 dev, 4 held-out. A perfect note solved
every one of them, so each of the 9 is solvable when the fact is available,
and failing without it.
