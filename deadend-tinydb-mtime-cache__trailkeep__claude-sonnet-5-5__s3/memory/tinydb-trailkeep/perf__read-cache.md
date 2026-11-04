# perf/read-cache

Branch: perf/read-cache · Repo: local__tinydb-4124091834 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: JSONStorage read cache: mtime-keyed invalidation was tried before and removed - db files on NFS with 1s mtime resolution served stale data when importer wrote within the same second. Don't key cache on mtime alone.
- 2026-11-04: JSONStorage read cache validates by comparing raw file text (not mtime/stat); deepcopy on hit was tried and is 4x slower than json.load (2.7s vs 0.65s on 40MB), so cached object is returned uncopied - callers mutating nested results alias the cache until next write/external change.

