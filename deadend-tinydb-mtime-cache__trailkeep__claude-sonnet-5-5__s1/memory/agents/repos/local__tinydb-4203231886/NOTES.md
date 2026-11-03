# Private notes: local__tinydb-4203231886

- 2026-11-03: Do not use an mtime-based cache for JSONStorage.read(): db files live on NFS with 1-second mtime resolution, so same-second writes by the importer served stale data (tried and removed last year). Any cache invalidation must not rely on mtime alone.
