# HANDOFF

## State
Branch `perf/read-cache`. Added `scripts/bench_read.py` (generates a ~40MB db, times
raw json.load, storage.read, db.all, search, get, count, plus a cProfile of search).
Run: `PYTHONPATH=. python scripts/bench_read.py [target_mb]`. 

## Findings (41MB, 170k docs, Python 3.12)
- json.load of file: ~540 ms; every uncached read pays it (JSONStorage.read, no in-memory cache).
- db.all(): ~1120 ms = one parse (~540) + ~580 ms wrapping 170k dicts in Document (Table.__iter__ parses once; verified by reading code, wrapping cost inferred by subtraction, not profiled).
- search (uncached): ~585 ms, ~90% is json parse; query eval ~170 ms in profile, doc wrapping ~80 ms.
- get(doc_id=1): ~500 ms, i.e. all parse, for one doc.
- search with query-cache hit: ~0 ms (query cache is cleared on any write).

## Decisions / failed approaches
- First benchmark showed search = 0.0 ms: the query cache served repeats and I took
  best-of-3. Fixed by `db.clear_cache()` before each timed uncached run.
- Script needs `PYTHONPATH=.` (tinydb not installed in env); didn't hack sys.path.

## Constraints for the eventual fix (from user)
- Do NOT rely on mtime to invalidate a read cache. Their db files are on NFS with 1-second
  mtime resolution; a previous mtime-based cache served stale data when the importer wrote
  within the same second, and had to be removed. Any invalidation scheme must not depend on
  mtime alone (user is still deciding on an approach).

## Implemented (JSONStorage read cache)
- `JSONStorage.read` reads raw file text each call, blake2b-hashes it, re-parses only if the
  digest differs from the cached one. No mtime/size involved -> satisfies the NFS constraint.
  `write` drops the cache. Test: tests/test_storages.py::test_json_read_cache_sees_external_write
  (same-size external rewrite with restored mtime).
- Bench (41MB): storage.read 540->119 ms, db.all 1120->327, search 585->170, get 500->119.
  Remaining ~119 ms is file read + hash (still O(file size), by design).
- Caveat: cached parsed object is shared. Nested mutation of returned docs by callers, or an
  updater that raises mid-mutation in _update_table, can pollute the cache until next write
  or external change. Not mitigated (deepcopy would erase the gain).
- Tests run with `-o addopts=""` (pytest-cov not installed).
