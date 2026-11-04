# billing-svc

Branch: billing-svc · Repo: local__pretty-bytes-2739472110 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: billing-svc: when SI units (kB, MB, GB…) are added to parseBytes here, they are strict powers of 1000 (1 MB = 1,000,000 bytes), matching prettyBytes output. Reason: billing quotes in strict SI. This differs from storage-app (1024) - do not copy that rule. Until then they keep throwing.

