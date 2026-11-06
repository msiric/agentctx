# storage-app

Branch: storage-app · Repo: local__pretty-bytes-2523841890 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: Storage team decision: in parseBytes on this branch, units without the 'i' (KB/kB, MB, GB...) are powers of 1024 (Windows Explorer style): '1 KB' and '1 kB' = 1024, '1 MB' = 1048576. Not implemented yet; they currently throw 'Unsupported unit' (test 'decimal units are not supported yet' must be replaced). Do not read them as powers of 1000. Binary units (KiB..YiB) done and committed.
- 2026-11-06: parseBytes units without the 'i' (kB/KB, MB..YB) are now implemented as powers of 1024 per the storage team decision, with tests and readme/index.d.ts docs; the 'not implemented yet' entry is outdated. Matching stays case-sensitive (e.g. 'mb' throws) - my choice, kept from the binary-unit work.

