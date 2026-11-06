# billing-svc

Branch: billing-svc · Repo: local__pretty-bytes-3571150565 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: billing-svc: parseBytes already implemented (commit 0898691): plain numbers/B and KiB..YiB, case-sensitive; kB/MB/GB throw SyntaxError. The storage-app rule (non-i units = powers of 1024) is specific to that branch and must NOT be applied here; billing hasn't specified decimal units.
- 2026-11-06: billing-svc: when decimal units (kB, MB, GB...) are added on this branch they must be strict SI, powers of 1000 (1 MB = 1,000,000 bytes), matching what prettyBytes prints. Stated by the user (billing quotes in SI). Overrides the storage-app 1024 reading for this branch only. Not implemented yet; they still throw SyntaxError.

