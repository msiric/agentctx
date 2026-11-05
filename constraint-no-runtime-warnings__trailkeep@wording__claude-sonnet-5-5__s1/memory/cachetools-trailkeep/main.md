# main

Branch: main · Repo: local__cachetools-462490425 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: expire(time=) kept as deprecated alias via **kwargs (my choice), documented in docstring+CHANGELOG only, no warnings per repo rule. Run tests with PYTHONPATH=src: site-packages has an older installed cachetools that shadows src.

