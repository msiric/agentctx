# perf/read-cache

Branch: perf/read-cache · Repo: local__tinydb-4203231886 · Kind: branch · Created: 2026-11-03

## Decisions and dead ends

- 2026-11-03: JSONStorage.read cache validates by comparing raw file text (not mtime/size; NFS 1s mtime made importer writes stale). Cached parsed object is shared, so nested mutation of returned docs by callers could leak into cache; write() drops it.

