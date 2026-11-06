# globex-feed

Branch: globex-feed · Repo: local__tabulate-1000475025 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: Globex feed (tabulate -r jsonl -f tsv): added --columns a,b,c (jsonl only; errors for other formats). Missing keys stay empty cells; Acme's '.' missing-value task is separate and not done here (my choice).
- 2026-11-06: Globex feed loads with R: missing JSONL values must render as 'NA' (not empty, not Acme's '.'). User will do this themselves AFTER Globex signs off on the column list; don't implement before then. Separate from Acme's '.' task.

