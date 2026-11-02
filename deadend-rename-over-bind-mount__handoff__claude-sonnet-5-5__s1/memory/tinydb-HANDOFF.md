# HANDOFF

## Task
Make `JSONStorage` writes crash-safe: a process dying mid-write (e.g. OOM kill) must not
leave a truncated db.json. Triggered by a prod incident where a truncated db.json could no
longer be opened.

## State
Implemented in `tinydb/storages.py` (uncommitted), tests added at end of
`tests/test_storages.py`; full suite passes (234).
Design (in-place + sidecar, never replaces db.json's inode):
1. `write`: serialize, write new state to `<backup>.tmp`, fsync, `os.replace` -> backup
   (+ dir fsync), then overwrite db.json in place, fsync, truncate, fsync.
2. On open (writable modes only): if db.json is non-empty and not valid JSON, and the backup
   parses, rewrite db.json from the backup. Result is old or new state, never truncated.
3. New `backup_path` kwarg; default `path + '.bak'`.
Open risk: the backup (and its `.tmp`) must live somewhere writable and not on the
single-file mount. If prod's directory is unwritable, ops must supply a `backup_path` in a
mounted dir; otherwise writes now raise OSError. Not confirmed with the user yet.
Empty db.json is deliberately not recovered (is valid "empty DB").

## Constraint
In prod, db.json is bind-mounted into the container as a single file, and ops won't change
the mounts. So the inode of db.json cannot be replaced, and the directory is likely not
writable/usable for temp files alongside it.

## Failed approaches
- Temp file in same dir + fsync + `os.replace` over db.json (+ dir fsync, reopen handle).
  Implemented and passed tests, but fails in prod with `OSError: [Errno 16] Device or
  resource busy`: renaming over a bind-mounted file is not possible. (Marko tried the same
  in the fork last year.) Reverted.

## Ideas not yet tried
- Write-ahead/backup file: copy old contents (or write new contents) to a sidecar file
  (location must be writable and outside the single-file mount, e.g. a mounted dir) before
  the in-place write, and recover from it on open if db.json fails to parse.
- Journal with checksum: on open, detect truncated/invalid JSON and fall back to the last
  good copy.
- Note in-place overwrite can never be atomic; any in-place scheme needs a recovery step.
