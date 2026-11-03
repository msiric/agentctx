# crash-safe-writes

Branch: crash-safe-writes · Repo: local__tinydb-722378169 · Kind: branch · Created: 2026-11-03

## Decisions and dead ends

- 2026-11-03: JSONStorage crash-safe writes: temp file + os.replace is NOT viable. Prod bind-mounts db.json as a single file, so rename over it fails with EBUSY (Errno 16); ops won't change mounts. Marko's fork hit the same. Reverted; need an in-place approach.
- 2026-11-03: JSONStorage crash safety implemented in place: checksummed sidecar <path>.journal (fsync'd) written before in-place rewrite, replayed on open if valid, discarded if torn. Caveat: needs a writable, persistent dir next to db.json (bind-mounted single file alone won't keep the journal across container restarts).

