# Private notes: local__cachetools-1945064594

- 2026-11-05: Nothing added to this fork may emit a warning at runtime (DeprecationWarning included): the ingest service vendors it and runs its test suite with -W error, and that team won't relax it. Deprecations go only in the docstring and CHANGELOG.rst, never warnings.warn.
