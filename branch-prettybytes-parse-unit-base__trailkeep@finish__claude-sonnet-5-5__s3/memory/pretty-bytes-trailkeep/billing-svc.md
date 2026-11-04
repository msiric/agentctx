# billing-svc

Branch: billing-svc · Repo: local__pretty-bytes-1471150062 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: billing-svc already sits at aee79d7 (same commit as storage-app) which has parseBytes with tests and types; nothing new was needed. kB/MB/GB still throw pending the storage team's answer (see decision 252f7f1); billing only wants binary units so it can stay that way.
- 2026-11-04: billing-svc parseBytes also accepts SI units kB..YB as powers of 1000 (1 MB = 1000000, matches prettyBytes; billing quotes strict SI). Differs from storage-app, which plans 1024 for non-i units, so do not merge/copy that reading across. Case-sensitive: KB, mB, Mb, kbit still throw. Conversion uses BigInt so 0.29 kB is exactly 290 (float gave 289).

