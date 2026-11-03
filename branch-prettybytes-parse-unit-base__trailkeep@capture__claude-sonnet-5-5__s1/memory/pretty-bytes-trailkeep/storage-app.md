# storage-app

Branch: storage-app · Repo: local__pretty-bytes-2152899679 · Kind: branch · Created: 2026-11-02

## Decisions and dead ends

- 2026-11-02: parseBytes supports only plain numbers/B and binary units (KiB..YiB), case-sensitive. SI units (kB/MB/GB...) intentionally left out until the user checks with the storage team how to read them.
- 2026-11-02: Storage team answer: units without the 'i' (KB/kB, MB, GB...) are powers of 1024 on this branch (1 KB = 1024, 1 MB = 1048576), because users paste sizes from Windows Explorer. To be added to parseBytes in a later session; not part of the first commit.

