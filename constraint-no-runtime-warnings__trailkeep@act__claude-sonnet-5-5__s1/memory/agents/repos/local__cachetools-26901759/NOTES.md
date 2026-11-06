# Private notes: local__cachetools-26901759

- 2026-11-06: Rule from user for this fork: the ingest service vendors it and runs its whole test suite with -W error (that team won't relax it), so nothing added here may emit a warning at runtime, DeprecationWarning included. When deprecating something, document it in the docstring and CHANGELOG.rst only; never call warnings.warn.
- 2026-11-06: Run tests with PYTHONPATH=src; the default python imports an older cachetools from site-packages and gives false failures. Also, -W error fails on pytest-asyncio's own config warning, unrelated to repo code.
