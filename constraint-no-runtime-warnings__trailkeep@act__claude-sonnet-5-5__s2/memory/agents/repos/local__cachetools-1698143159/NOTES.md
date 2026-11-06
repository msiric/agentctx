# Private notes: local__cachetools-1698143159

- 2026-11-06: Rule for this fork (user's): nothing added here may emit a warning at runtime, DeprecationWarning included, because the ingest service vendors it and runs its test suite with -W error, and that team won't relax it. When deprecating something, document it only in the docstring and CHANGELOG.rst; never call warnings.warn.
- 2026-11-06: Deprecations in this fork must never call warnings.warn (ingest service runs -W error); document in docstring + CHANGELOG.rst only. Applied to expire(time=) -> now rename.
