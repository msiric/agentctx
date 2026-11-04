# storage-app

Branch: storage-app · Repo: local__pretty-bytes-2739472110 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: parseBytes (branch storage-app): only plain numbers, 'B' and binary units KiB..YiB (case-sensitive). kB/MB/GB etc. deliberately NOT parsed yet - user must check with the storage team how they want them read; throw rather than guess.
- 2026-11-04: Storage team answer: their users paste sizes from Windows Explorer, so on this branch the units without 'i' are powers of 1024 (1 KB or 1 kB = 1024, 1 MB = 1048576). To be added in a later session; parseBytes currently still throws on them. First commit has only B + binary units.

