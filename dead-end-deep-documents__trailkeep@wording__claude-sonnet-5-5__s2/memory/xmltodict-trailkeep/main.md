# main

Branch: main · Repo: local__xmltodict-2784250864 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: drop_keys in xmltodict.py is deliberately iterative (explicit stack): catalog test feed nests <part> ~3000 deep and recursive walks hit RecursionError. Keep any further tree helpers iterative. Uncommitted as of now.

