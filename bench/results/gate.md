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

# Headroom gate, batch 2 (2026-11-02)

Same rule, same model, run 41446572859.

| Trap | Split | none | oracle-note | Verdict |
|---|---|---|---|---|
| branch-prettybytes-parse-unit-base | dev | 0/3 | 3/3 | keep |
| deadend-rename-over-bind-mount | dev | 0/3 | 3/3 | keep |
| deadend-sortkeys-mixed-keys | dev | 0/3 | 3/3 | keep |
| superseded-prettybytes-lenient-options | dev | 0/3 | 3/3 | keep |
| xrepo-error-prefix-prettybytes-to-cookie | dev | 0/3 | 3/3 | keep |
| xrepo-version-bump-cookie-to-ms | dev | 0/3 | 3/3 | keep |
| decision-csv-excel-dialect | held-out | 0/3 | 3/3 | keep |
| superseded-ms-compound-go-duration | held-out | 0/3 | 3/3 | keep |
| constraint-scheduler-private-rng | dev | 3/3 | 3/3 | drop: no headroom |
| decision-heartbeat-epoch-ms | dev | 3/3 | 3/3 | drop: no headroom |
| constraint-no-error-level-logs | held-out | 3/3 | 3/3 | drop: no headroom |
| branch-ms-month-uppercase-m | held-out | 0/3 | 1/3 | drop: broken |

`branch-ms-month-uppercase-m` failed with the perfect note because its check
also requires the unit spelling `mo`, which the task never asks for. The
rule drops it; it is not edited.

The revised brief worked better: 8 of 12 kept, against 9 of 12 in batch 1,
and every kept trap has none at 0/3.

# Totals after both batches

17 fact traps kept: 11 dev, 6 held-out. Plus 2 controls (1 dev, 1 held-out).

- dev: branch-ms-iso-no-regex, branch-prettybytes-parse-unit-base,
  crossrepo-table-driven-tests, deadend-rename-over-bind-mount,
  deadend-sortkeys-mixed-keys, decision-schedule-reraise,
  superseded-ms-invalid-returns-undefined, superseded-prettybytes-lenient-options,
  superseded-ufo-same-origin-ports, xrepo-error-prefix-prettybytes-to-cookie,
  xrepo-version-bump-cookie-to-ms; control-scule-constant-case
- held-out: constraint-schedule-no-module-shortcuts, crossrepo-no-positional-booleans,
  deadend-tinydb-mtime-cache, decision-csv-excel-dialect, decision-tinydb-yaml-bools,
  superseded-ms-compound-go-duration; control-dotenv-get-default

# Headroom gate, held-out set 2 (2026-11-04)

Same rule, same model, frozen versions, run 41836429541. Every set-2 trap is
held-out (PREREGISTRATION.md, addendum).

| Trap | none | oracle-note | Verdict |
|---|---|---|---|
| branch-isolation-fiscal-quarter | 0/3 | 3/3 | keep |
| branch-isolation-semver-silent-deprecation | 0/3 | 3/3 | keep |
| constraint-fork-upstream-files | 0/3 | 3/3 | keep |
| cross-repo-doctest-examples | 1/3 | 3/3 | keep |
| cross-repo-version-bump | 0/3 | 3/3 | keep |
| dead-end-humanize-half-up | 0/3 | 3/3 | keep |
| dead-end-inject-encoding | 0/3 | 3/3 | keep |
| decision-schema-length-bytes | 0/3 | 3/3 | keep |
| decision-week-numbering | 0/3 | 3/3 | keep |
| superseded-semver-json-output | 0/3 | 3/3 | keep |
| superseded-test-runner | 0/3 | 3/3 | keep |
| constraint-schema-no-values-in-errors | 3/3 | 3/3 | drop: no headroom |

11 of 12 kept. The perfect note passed every kept trap 3/3.
