# Private notes: local__tinydb-2077454173

- 2026-11-04: Do not use temp-file + os.replace for JSONStorage crash safety: prod bind-mounts db.json as a single file, so rename over it fails with OSError EBUSY (Errno 16), and ops won't change the mounts. Marko tried this in the fork last year. Need an in-place approach (e.g. journal/backup + fsync).
- 2026-11-04: JSONStorage crash safety uses a sibling <path>.journal (sha256-checksummed) + in-place overwrite + replay on open; no temp-file/os.replace because prod bind-mounts db.json (EBUSY). Requires the db's directory to be writable for the journal file.
