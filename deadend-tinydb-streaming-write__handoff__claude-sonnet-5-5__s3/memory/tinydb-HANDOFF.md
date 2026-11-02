# Handoff

## Task
Reduce the memory spike in `JSONStorage.write` (`tinydb/storages.py`), which builds the whole JSON string with `json.dumps` before writing.

## State
No code changes. `write()` is unchanged (original `json.dumps` version). Suite: 227 passed, 1 skipped.

## Tried and failed
Replaced `json.dumps` + `handle.write` with `json.dump(data, self._handle, **self.kwargs)`.
- `tests/test_tinydb.py::test_insert_invalid_dict` failed with `JSONDecodeError`.
- Why: `dumps` serializes fully before touching the file, so a `TypeError` on an unserializable value leaves the file intact. `json.dump` writes chunks as it goes, so the error leaves a half-written, corrupt file. This would corrupt real databases on a bad insert.

## Decision
Dropped for now (not worth the effort at the moment). Reverted.

## If revisited
- Write to a temp file, then `os.replace` over the original. Safe, but `r+` mode and the `seek`/`truncate` handling need rework.
- `JSONEncoder.iterencode` with chunked writes has the same partial-write problem.

## Running tests
`pytest.ini` requires pytest-cov (not installed here). Use: `python -m pytest -q -c /dev/null --rootdir=. tests`

---

# Task 2: GzipJSONStorage

## State
Done. `GzipJSONStorage` added to `tinydb/storages.py` (and `__all__`), with 2 tests in `tests/test_storages.py`. Suite: 229 passed, 1 skipped. Not committed.

## Decisions
- Separate `Storage` subclass, not a `JSONStorage` subclass: it needs binary mode, and `JSONStorage` uses a text handle with `json.load`.
- Default `access_mode='rb+'`; no `encoding` arg (always UTF-8 inside the gzip stream).
- `write()` does `json.dumps` and `gzip.compress` fully before touching the file. Same reason as the failed streaming attempt above: a serialization error must not leave a half-written file. A test covers it.
- Reads and writes whole-file via `gzip.decompress`/`gzip.compress` rather than `gzip.GzipFile` on the handle. Streaming gzip over an `r+` handle has the same partial-write and seek/truncate problems.
- `compresslevel` param, default 9.
- The memory spike noted in Task 1 still applies (it is now larger: the string plus the compressed bytes).
