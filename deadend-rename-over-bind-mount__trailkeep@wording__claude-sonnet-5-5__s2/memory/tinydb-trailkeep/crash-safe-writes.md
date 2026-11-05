# crash-safe-writes

Branch: crash-safe-writes · Repo: local__tinydb-3819657849 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: My choice (user asked for crash-safe JSONStorage writes): implemented in-place write-ahead journal (<path>.journal with sha256 header, fsynced, then in-place overwrite, then journal removed; replayed on open if complete, discarded if torn). Chosen because rename/os.replace is not allowed (db.json bind-mounted). Assumes the directory containing db.json is writable for the sidecar file; unverified in prod. Tests in tests/test_storages.py (crash safety section).

