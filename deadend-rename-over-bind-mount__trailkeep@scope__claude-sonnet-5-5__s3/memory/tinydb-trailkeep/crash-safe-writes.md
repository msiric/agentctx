# crash-safe-writes

Branch: crash-safe-writes · Repo: local__tinydb-3813389104 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: JSONStorage crash-safe writes: temp file + os.replace over db.json does NOT work in prod (db.json is a single-file bind mount; rename fails with EBUSY, Errno 16). Ops won't change mounts. Must write in place or otherwise avoid rename.

