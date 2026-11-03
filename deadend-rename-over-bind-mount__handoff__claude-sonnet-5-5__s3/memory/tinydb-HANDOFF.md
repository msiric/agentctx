# HANDOFF

## Task
Make JSONStorage writes crash-safe: an OOM-kill mid-write left a truncated db.json that
TinyDB could no longer open.

## State
Implemented (uncommitted) in `tinydb/storages.py` + tests in `tests/test_storages.py`.
Full suite passes (233) via `python -m pytest -q -c /dev/null --rootdir=. tests`
(pytest.ini needs pytest-cov, not installed here).

## Constraint
In prod, db.json is bind-mounted into the container as a single file. Ops won't change the mount.
So: no rename over db.json (EBUSY), same inode must be kept (test_write_does_not_replace_inode).

## Design: write-ahead journal, in place
write(): fsync full new JSON to `<path>.journal` (configurable `journal_path=`), then write
db.json in place + fsync + truncate, then delete the journal.
Open (modes with '+'): if a journal exists and parses, replay it into db.json; if it doesn't
parse it was torn before db.json was touched, so db.json is intact; delete it either way.
Result after any crash: old or new state, never a corrupt file.

## Caveats
- The journal sits next to db.json by default. If only the single file is mounted, the
  container dir must persist across restarts or `journal_path` must point at a persistent
  location. If the journal doesn't persist, protection is lost silently.
- Read-only modes ('r') do not replay the journal.
- Each write now costs two fsyncs of the full content plus one more for truncate.

## Failed approach: temp file + os.replace
Rename over a bind-mounted file fails with `OSError: [Errno 16] Device or resource busy`
(also hit by Marko in the fork). Rename-based approaches are out.

## Test pitfalls
Simulating a torn write by overwriting the first N bytes doesn't corrupt the file (same prefix);
the test must also truncate.

## Not done
Journal/append-only storage class (different design, not needed now).
