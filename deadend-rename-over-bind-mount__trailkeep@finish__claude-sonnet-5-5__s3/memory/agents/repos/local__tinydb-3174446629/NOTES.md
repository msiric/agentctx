# Private notes: local__tinydb-3174446629

- 2026-11-04: Don't make JSONStorage crash-safe via temp file + os.replace: prod bind-mounts db.json as a single file, so rename over it fails with EBUSY (Errno 16). Ops won't change the mounts. Need an in-place approach (e.g. journal/backup copy).
- 2026-11-04: JSONStorage crash safety is an in-place journal (<db>.journal: sha256 line + payload, written+fsynced before overwriting db.json, replayed on open if valid, discarded if incomplete). Chosen because temp file + os.replace fails with EBUSY on prod's single-file bind mount. Caveat: the journal is a sibling file, so the db directory must be writable/persistent in prod.
