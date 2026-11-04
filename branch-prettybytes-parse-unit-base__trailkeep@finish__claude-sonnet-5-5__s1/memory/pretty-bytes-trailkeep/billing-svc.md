# billing-svc

Branch: billing-svc · Repo: local__pretty-bytes-4148375603 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: billing-svc pins this branch: parseBytes supports plain numbers and binary units (B, KiB..YiB) only; decimal kB/MB/GB deliberately unsupported for now (billing asked). Branch is at the same commit as storage-app (da12924); storage team's 1024-based reading of KB/MB is a storage-app decision, not adopted here.
- 2026-11-04: billing-svc: when decimal units are added, they are strict SI: 1 kB = 1000, 1 MB = 1,000,000 bytes, matching prettyBytes' non-binary output. Reason: billing quotes in strict SI. Differs from storage-app, which reads KB/MB as 1024 powers.

