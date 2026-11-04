# Private notes: local__tinydb-976997440

- 2026-11-04: Do not make JSONStorage.write crash-safe via temp file + os.replace/rename: prod bind-mounts db.json as a single file, so rename over it fails with OSError EBUSY (Errno 16), and ops won't change the mounts. Marko tried this in the fork and hit the same thing. Any fix must write in place.
