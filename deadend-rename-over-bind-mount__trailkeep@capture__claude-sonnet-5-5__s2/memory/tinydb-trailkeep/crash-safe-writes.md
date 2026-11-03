# crash-safe-writes

Branch: crash-safe-writes · Repo: local__tinydb-362681528 · Kind: branch · Created: 2026-11-03

## Decisions and dead ends

- 2026-11-03: Crash-safe JSONStorage via temp file + os.replace was tried and backed out: prod bind-mounts db.json as a single file, so rename over it fails with EBUSY (Errno 16). Ops won't change mounts; need an in-place approach (e.g. journal/backup copy).
- 2026-11-03: Crash-safe JSONStorage now uses in-place write + sha256-checksummed sidecar '<path>.journal' (no rename, so bind-mounted db.json works); recovery replays complete journal on open, discards partial one. Journal lives next to db.json: needs that dir writable/persistent.

