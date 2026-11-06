# globex-feed

Branch: globex-feed · Repo: local__tabulate-1484260429 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: Globex feed (R loader): missing values must output as 'NA' (not empty). User will implement after Globex signs off on the column list; NOT started. --columns already committed (9424e8c). Note: acme-feed branch wants '.' for missing instead, so make missing-value token per-branch/option, not a global default.

