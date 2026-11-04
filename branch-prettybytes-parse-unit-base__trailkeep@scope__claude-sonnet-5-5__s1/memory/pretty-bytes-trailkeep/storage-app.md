# storage-app

Branch: storage-app · Repo: local__pretty-bytes-2012026554 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: parseBytes: storage team confirmed (users paste sizes from Windows Explorer) that on this branch units without the 'i' are powers of 1024: '1 KB' or '1 kB' = 1024, '1 MB' = 1048576. Not implemented yet; currently these throw SyntaxError. Add next.

