# main

Branch: main · Repo: local__cachetools-1945064594 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: expire(): renamed time->now; legacy time= kept as keyword-only alias (no warnings.warn, per repo rule); deprecation documented in docs/index.rst + CHANGELOG. Tests must run with PYTHONPATH=src (site-packages has an installed cachetools).

