# Handoff: crash-safe JSONStorage writes

## State
Implemented in `tinydb/storages.py` (write-ahead journal), tests in
`tests/test_storages.py` (`test_json_crash_safe*` etc.). Full suite passes
(run with `-c /dev/null --rootdir .`; pytest.ini needs pytest-cov, absent here).

## Design (db.json is always modified in place, same inode)
- `write`: serialize -> write `sha256\n<payload>` to sidecar journal
  (`path + '.journal'`, or `journal_path=`) + fsync -> in-place write ->
  truncate -> fsync (fsync moved after truncate; before, a crash between
  left new-prefix+old-tail).
- `read`: if db.json fails to parse and journal checksum is valid, return the
  journal state and (if writable mode) restore db.json in place.
- Journal is complete before db is touched, so torn journal => db is intact.
- Journal unwritable => one-time warning at first write, writes unprotected.
  (Journal is not created at init: test_create_dirs rmdir's the dir.)

## Decisions / gotchas
- Wrong-encoding reads fail JSON parse too; without a guard recovery would
  overwrite a healthy file (test_encoding caught this). `_looks_like_same_file`
  compares the first <=8 raw bytes of file vs journal encoded in the handle's
  encoding.
- Recovery only on unparsable db, not on empty db (could resurrect deleted data).
- Cost: every write is doubled (journal + db), both fsynced.
- Journal lives next to db by default; in prod with a single-file mount the
  dir may be unwritable -> must pass `journal_path` to a writable location.

## Failed approach: atomic rename over db file
`os.replace` onto db.json fails with EBUSY: prod bind-mounts the single file.
Ops won't change mounts. Hence in-place + journal.
