# crash-safe-writes

Branch: crash-safe-writes · Repo: local__tinydb-3804887958 · Kind: branch · Created: 2026-11-02

## Decisions and dead ends

- 2026-11-02: Atomic write via temp file + os.replace in JSONStorage does NOT work for us: prod bind-mounts db.json as a single file, so rename fails with EBUSY (Errno 16); ops won't change mounts. Marko tried this in the fork too. Backed out.
- 2026-11-02: Crash-safe JSONStorage: in-place write + sidecar <path>.journal (sha256 + payload, fsynced before touching db.json), replayed on open if checksum valid, torn journal discarded. No rename of db.json (EBUSY on bind mount). Requires the db's directory to be writable/persistent for the journal.

