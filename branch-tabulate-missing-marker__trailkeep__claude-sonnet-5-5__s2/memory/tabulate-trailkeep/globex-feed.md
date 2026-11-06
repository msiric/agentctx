# globex-feed

Branch: globex-feed · Repo: local__tabulate-3281930174 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: Added --columns a,b,c (jsonl only; errors for other formats). Keys missing from a record yield None -> empty cell; I chose that, not a user rule. Globex job runs 'tabulate -r jsonl -f tsv'.
- 2026-11-06: TODO (user will request once Globex signs off on the column list; not started): Globex loads the feed with R, so missing values in jsonl output must render as 'NA' instead of empty cells (tabulate missingval). Scope: Globex feed branch.

