# HANDOFF

## Task
Reduce memory spikes when writing big DB files: `JSONStorage.write` (tinydb/storages.py) built the whole string with `json.dumps`.

## Current state
**Reverted.** `write()` is back to the original `json.dumps` version; user decided the fix isn't worth it right now. Only this file is uncommitted.

What was tried: replaced `json.dumps` + `handle.write` with `json.dump(data, self._handle, **self.kwargs)` inside the existing `try/except io.UnsupportedOperation`.

Tests (`python -m pytest -q -c /dev/null --rootdir=. tests`; the repo's pytest.ini needs pytest-cov) with that change: 226 passed, 1 skipped, **1 failed**. Baseline is 227 passed, 1 skipped.

## Failure and why
`tests/test_tinydb.py::test_insert_invalid_dict`: a non-serializable value now raises TypeError midway through writing, after part of the JSON is already in the file. The file is left corrupted, and the next read raises JSONDecodeError. `dumps` failed before touching the file, so the old code was safe here.

## Not done / options
- Not pursued yet (user asked to stop after testing). Possible fixes: write to a temp file and atomically replace it (changes the open-handle design), or snapshot the original contents and restore them on failure. Either has a cost, so this needs the user's call.
- Memory benefit was not measured.

---

# Task 2: GzipJSONStorage
## Current state
Done, uncommitted. `GzipJSONStorage(JSONStorage)` in tinydb/storages.py (added to `__all__`), test `test_gzip_json` in tests/test_storages.py. Suite: 228 passed, 1 skipped.

## Decisions
- Subclasses JSONStorage, opens file in `rb+` (binary required; ValueError otherwise). Reuses `touch`/open logic.
- Whole file is compressed/decompressed per write/read (gzip stream can't be updated in place); `compresslevel` param, default 9.
- `write` uses `json.dumps` then compress *before* touching the file, so a non-serializable value can't corrupt it (the lesson from Task 1's failed `json.dump` attempt).
- Empty file reads as `None`.
- Compression ratio (~10x) not measured here.
