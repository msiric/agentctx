# perf/read-cache

Branch: perf/read-cache · Repo: local__tinydb-2465908374 · Kind: branch · Created: 2026-11-03

## Decisions and dead ends

- 2026-11-03: Read cache for JSONStorage: do NOT key on mtime (or mtime+size) alone. DB files are on NFS with 1s mtime resolution; a prior mtime-based cache served stale data when the importer wrote within the same second and was removed. scripts/bench_read.py has baseline numbers.
- 2026-11-03: JSONStorage read cache: compares full raw file contents (exact, no mtime/size) and caches a marshal snapshot, returning a fresh copy per read, because Table._update_table mutates read() results and Document copies only the top level; sharing the parsed object was rejected as unsafe. Gain is modest (~35% on cache hit, 40MB: json.loads 460ms vs marshal.loads 280ms).

