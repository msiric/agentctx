# HANDOFF

## Current task: GzipJSONStorage
Added `GzipJSONStorage` to tinydb/storages.py (exported in `__all__`) plus `test_gzip_json` in tests/test_storages.py.
Suite: 228 passed, 1 skipped (run with `python -m pytest -c /dev/null --rootdir=. tests`; the repo's pytest.ini needs pytest-cov).

Decisions:
- Opens the file in binary mode (`r+b`); reads the whole file, `gzip.decompress`, `json.loads`. Empty file -> `None`.
- `write` serializes with `json.dumps` and compresses *before* touching the file, so an unserializable value raises without corrupting the file (see the failed approach below).
- Extra `compresslevel` arg (default 9); other kwargs go to `json.dumps`.
- Not documented in docs/ yet.

## Earlier task (parked): memory spike in `JSONStorage.write`
Tried replacing `json.dumps` + `write` with streaming `json.dump`; reverted. It fails `tests/test_tinydb.py::test_insert_invalid_dict`: on an unserializable value, `json.dump` has already written a partial document before raising TypeError, leaving a corrupt file. User decided not to pursue now. If revisited: write to a temp file and atomically replace.
