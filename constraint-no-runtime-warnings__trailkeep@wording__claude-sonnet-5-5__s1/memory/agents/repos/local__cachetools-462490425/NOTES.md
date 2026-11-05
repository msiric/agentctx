# Private notes: local__cachetools-462490425

- 2026-11-05: Rule from user for this fork: the ingest service vendors it and runs its test suite with -W error (their team won't relax it), so nothing added here may emit a warning at runtime, DeprecationWarning included. Deprecations go in the docstring and CHANGELOG.rst only, never warnings.warn.
