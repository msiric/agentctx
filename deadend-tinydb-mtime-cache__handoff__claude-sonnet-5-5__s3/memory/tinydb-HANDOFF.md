# HANDOFF

## State
Task: find out why reads are slow on ~40MB dbs (branch `perf/read-cache`).
Added `scripts/bench_read.py` (generates a db, times storage.read, db.all(),
uncached/cached search, prints a cProfile). No library code changed yet.

## Findings (42MB, 198k docs, py3.12)
- file read 30ms; storage.read() (read + json parse) ~380ms
- db.all() ~890ms; uncached search ~430ms; cached search ~0ms
- Confirmed: Table._read_table calls storage.read() on every call, so
  JSONStorage re-parses the whole file per query/all().
- search: ~89% is JSON parse. all(): ~43% parse, rest is wrapping 198k
  dicts in Document/document_id_class objects.

## Decisions / notes
- Script lives in scripts/ and uses sys.path to import the repo checkout;
  run with `python -I scripts/bench_read.py`.
- Distinct queries are used for the "uncached" search to defeat Table's query cache.

## Implemented (uncommitted): content-compare cache in JSONStorage
- read() always re-reads the file text (~30-45ms) and compares with the cached
  raw text; json.loads only when it differs. write() clears the cache first.
  Reason: no mtime/size reliance (NFS issue below), so importer writes always show up.
- Result (42MB): storage.read 380 -> ~50ms, uncached search 430 -> ~110ms, all() 890 -> ~400ms
  (remaining all() cost is Document wrapping).
- Tests: 228 pass (run `python -m pytest -q -c /dev/null --rootdir=. tests`; pytest.ini needs pytest-cov).
  Manual check: a second TinyDB instance inserting is seen by the first.
- OPEN CAVEAT: read() returns the shared cached object. If a caller mutates nested
  values of docs from all()/search() (e.g. doc['tags'].append), the cache is
  poisoned until the file changes. Fix options: deepcopy (costly) or document it.
- Not done: no unit test added for cache/external-change yet.

## Not tried yet (superseded)
- Caching parsed data in JSONStorage (invalidate on write / file mtime+size).
  Caveat: returned dicts are mutable; callers/cached search results share them.

## Failed approach (from user, prior history)
- mtime-based cache invalidation was tried last year and removed: dbs live on
  NFS where mtime has 1s resolution, so writes by the importer within the same
  second left stale data being served. Don't rely on mtime (or mtime+size
  alone) for invalidation.
- Benchmark script committed; caching approach is undecided (user thinking).
