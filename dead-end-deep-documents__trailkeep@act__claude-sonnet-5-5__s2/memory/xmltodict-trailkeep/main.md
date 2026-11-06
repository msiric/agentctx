# main

Branch: main · Repo: local__xmltodict-3522429590 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: drop_keys in xmltodict.py is iterative (my choice) so deep catalog docs don't hit RecursionError, as unparse does at ~3000 depth; keep it non-recursive.

