# main

Branch: main · Repo: local__cachetools-26901759 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: My choice: expire() renamed time->now; 'time' kept as keyword-only alias, deprecated in docstring and CHANGELOG only (no warnings.warn, per the repo's no-warnings rule). Remove the alias in a later release.

