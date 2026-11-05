# Private notes: local__cachetools-3268953760

- 2026-11-05: Fork rule: nothing added here may emit a runtime warning (DeprecationWarning included), because the ingest service vendors this and runs its tests with -W error and won't relax it. Deprecations go only in the docstring and CHANGELOG.rst.
