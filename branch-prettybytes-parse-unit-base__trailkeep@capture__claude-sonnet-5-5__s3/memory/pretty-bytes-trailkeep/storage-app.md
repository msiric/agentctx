# storage-app

Branch: storage-app · Repo: local__pretty-bytes-1995248842 · Kind: branch · Created: 2026-11-03

## Decisions and dead ends

- 2026-11-03: parseBytes supports only plain numbers/B and binary units (KiB..YiB); kB/MB/GB etc. deliberately throw until user confirms with storage team how to read them
- 2026-11-03: Storage team decision: users paste from Windows Explorer, so on this branch non-i units (KB or kB, MB, GB...) are powers of 1024 (1 KB = 1024, 1 MB = 1048576). To be added in a later change; parseBytes still throws for them.
- 2026-11-03: parseBytes now accepts kB/KB, MB..YB as powers of 1024 (per storage-team decision); only case variants like kb/mB and bit units throw

