# Private notes: local__tinydb-2856257396

- 2026-11-04: JSONStorage: do NOT make writes crash-safe via temp file + os.replace. Prod bind-mounts db.json as a single file, so rename over it fails with OSError Errno 16 (Device or resource busy); ops won't change the mounts. Marko's fork tried this too. Need an in-place approach instead.
- 2026-11-04: JSONStorage crash safety uses a '<db>.journal' sidecar (write new state to journal+fsync, overwrite in place, delete journal; replay valid journal on open). Not temp+os.replace: prod bind-mounts db.json as a single file so rename fails (EBUSY). Caveat: journal lives next to db.json, so it must be on a writable, persistent dir.
