# billing-svc

Branch: billing-svc · Repo: local__pretty-bytes-2152899679 · Kind: branch · Created: 2026-11-02

## Decisions and dead ends

- 2026-11-02: Billing (billing-svc) quotes in strict SI: when SI units (kB, MB, GB...) are added to parseBytes here, 1 MB must be exactly 1,000,000 bytes (powers of 1000), matching prettyBytes output. This differs from storage-app, where KB/MB/GB are powers of 1024. Until then SI units stay rejected.

