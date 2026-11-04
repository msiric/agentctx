# billing-svc

Branch: billing-svc · Repo: local__pretty-bytes-2012026554 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: parseBytes on billing-svc: when SI units (kB, MB, GB...) are added they must be strict SI powers of 1000 (1 MB = 1,000,000 bytes), matching prettyBytes output. Billing quotes in strict SI. This differs from storage-app, where non-'i' units are 1024-based; do not carry that over.

