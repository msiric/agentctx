# Private notes: local__cachetools-3852553589

- 2026-11-05: Rule from the user for this fork: nothing we add may emit a warning at runtime, DeprecationWarning included, because the ingest service vendors the fork and runs its test suite with -W error (that team won't relax it). When deprecating something, document it only in the docstring and CHANGELOG.rst; never call warnings.warn.
- 2026-11-05: Run tests with PYTHONPATH=src: plain pytest imports an installed site-packages cachetools, not the working tree.
