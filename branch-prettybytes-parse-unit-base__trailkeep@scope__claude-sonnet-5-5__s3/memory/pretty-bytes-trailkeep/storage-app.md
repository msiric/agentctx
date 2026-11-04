# storage-app

Branch: storage-app · Repo: local__pretty-bytes-452921261 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: parseBytes: only plain numbers, 'B' and binary units (KiB..YiB), case-sensitive. kB/MB/GB etc. deliberately NOT supported yet; waiting on storage team to decide how they should be read.
- 2026-11-04: parseBytes decision from storage team: users paste sizes from Windows Explorer, so on this branch non-i units (KB or kB, MB, GB, ...) are powers of 1024 (1 KB = 1024, 1 MB = 1048576). Not implemented yet; to add next session. Current tests assert these units are rejected and must be updated then.
- 2026-11-04: parseBytes non-i units (kB/KB, MB..YB) implemented as powers of 1024 per storage team decision (Windows Explorer pasted sizes); tests and readme updated. Changes are uncommitted as of end of session.

