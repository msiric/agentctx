# acme-feed

Branch: acme-feed · Repo: local__tabulate-3281930174 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: Next task on this branch (not started; blank-line fix ships first, separately): jsonl records missing keys currently render as empty cells. Acme's loader is a SAS job and a missing value in SAS is a single '.', so those cells must be '.' instead of empty.
- 2026-11-06: Implemented: jsonl reader in tabulate/cli.py passes missingval='.' by default (no flag needed, cron uses 'tabulate -r jsonl -f tsv'); other readers unchanged (my choice). Test added in test/test_cli.py.

