# billing-svc

Branch: billing-svc · Repo: local__pretty-bytes-452921261 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: billing-svc: when kB/MB/GB.. are added to parseBytes, they must be strict SI (1 MB = 1,000,000 bytes, matching prettyBytes output), because billing quotes in strict SI. Not the 1024 reading from storage-app. Not implemented yet; only plain numbers, B and KiB..YiB for now.

