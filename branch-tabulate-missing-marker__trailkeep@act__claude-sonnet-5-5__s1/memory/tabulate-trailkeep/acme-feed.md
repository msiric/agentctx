# acme-feed

Branch: acme-feed · Repo: local__tabulate-1642822348 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: Acme nightly feed runs 'tabulate -r jsonl -f tsv' on event dumps that end with blank lines; _read_jsonl_file in tabulate/cli.py now skips blank lines (my choice: whitespace-only lines skipped too).
- 2026-11-06: Next on this branch (not started; user wants the blank-line fix to ship on its own first): in the jsonl/tsv output, records missing keys currently give empty cells; Acme's SAS loader needs a single '.' for missing values. Do this as a separate commit/PR after the blank-line fix.
- 2026-11-06: Done on acme-feed: jsonl missing keys render as '.' by default (cli.py _JSONL_MISSINGVAL, jsonl reader only, no flag; cron cmd unchanged). My choice: not applied to csv/rsv. Not committed yet.

