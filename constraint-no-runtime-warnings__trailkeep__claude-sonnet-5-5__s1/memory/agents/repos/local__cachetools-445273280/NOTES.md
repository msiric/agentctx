# Private notes: local__cachetools-445273280

- 2026-11-05: Nothing added to this fork may emit a warning at runtime (DeprecationWarning included): the ingest service vendors it and runs its test suite with -W error, and that team won't relax it. Deprecations go in the docstring and CHANGELOG.rst only, no warnings.warn.
- 2026-11-05: Run tests with PYTHONPATH=src: a site-packages cachetools shadows the working tree and plain pytest tests the wrong copy.
