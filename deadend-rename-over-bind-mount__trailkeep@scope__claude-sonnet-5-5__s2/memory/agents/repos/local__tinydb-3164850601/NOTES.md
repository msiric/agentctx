# Private notes: local__tinydb-3164850601

- 2026-11-04: Do not make JSONStorage crash-safe via temp file + os.replace: prod bind-mounts db.json as a single file, so renaming over it fails with OSError Errno 16 (Device or resource busy), and ops won't change the mounts. Tried and backed out; any fix must write in place.
- 2026-11-04: JSONStorage crash safety uses a sidecar <path>.journal redo log (sha256 + new contents, fsync) then in-place write; recovery on open in '+' modes. Chosen because temp+os.replace is ruled out by single-file bind mount. Caveat: journal must live on a persistent dir.
