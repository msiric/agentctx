# HANDOFF

## Task
User reports slow reads on ~40MB db files; suspected JSONStorage re-parses the file on every query. Asked for a benchmark under scripts/ and an explanation of where time goes.

## State
- Added `scripts/bench_read.py` (run: `PYTHONPATH=. python scripts/bench_read.py [MB] [repeat]`; PYTHONPATH needed because the script dir, not the repo root, is on sys.path).
- No library code changed. Not committed.

## Findings (42 MB, 288k docs, Python 3.12)
- storage.read (json.load): ~500 ms, paid on EVERY read call (`Table._read_table` -> `JSONStorage.read`, no caching).
- db.all(): ~1170 ms = parse + building 288k Document objects.
- db.search uncached: ~720 ms; db.get(doc_id=1): ~550 ms (almost all parse).
- Repeated identical search: ~0 ms (query cache), but cache is cleared on writes.

## Decisions / notes
- Benchmark uses a fresh query each iteration to defeat the query cache.
- No fix attempted yet; candidate: CachingMiddleware or a mtime-validated read cache in JSONStorage (branch name perf/read-cache). Needs care re: mutation of cached dicts.

## Failed approaches (from user)
- mtime-validated read cache: tried last year and removed. DBs live on NFS with 1-second mtime resolution, so writes by the importer within the same second as a cached read left stale data being served. Do NOT rely on mtime alone (size/inode also weak). Any new cache needs a different invalidation scheme or explicit opt-in.

## Status update
- Benchmark script committed on perf/read-cache; HANDOFF.md left uncommitted. User is deciding on the fix approach.

## Implementation (this session, uncommitted)
- `JSONStorage(cache_reads=True)` (opt-in, default off): reads file bytes each call, blake2b content hash; re-parses only if hash differs. No mtime/size/inode, per the NFS failure above -> importer writes always visible.
- `write()` drops cache first; `Table._update_table` calls `storage.invalidate_read_cache()` if the updater raises (updater mutates the cached dict in place). Returned data is shared: callers must not mutate it (documented).
- Tests added in tests/test_storages.py (same-size external write with restored mtime; failed update not served). Full suite: 230 pass (run `python -m pytest -c /dev/null --rootdir=. tests`; pytest.ini needs pytest-cov).
- Measured ~300k docs: db.get 277 ms -> 119 ms. Remaining cost = reading + hashing the whole file; skipping that needs a cheap change signal, which NFS doesn't give reliably.
- Opt-in rather than default because of shared-object mutation semantics.
