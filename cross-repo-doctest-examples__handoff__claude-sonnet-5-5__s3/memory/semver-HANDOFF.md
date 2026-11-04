# HANDOFF
- Added `Version.is_prerelease` (src/semver/version.py), `is not None` check on `_prerelease`.
- Tests: tests/test_is_prerelease.py. Changelog: changelog.d/pr505.feature.rst (PR number is a guess).
- Docstring has a runnable `>>>` example (user wants this for every new public API; saved in global CLAUDE.md).
- Running tests: needs `PYTHONPATH=src python -m pytest -c /dev/null --rootdir=. tests` (.pytest.ini wants coverage plugins not installed). Full suite: 515 passed.
- `--doctest-modules src/semver/version.py` run directly shows 12 failures that predate this change (likely need repo's doctest namespace setup); not investigated.
- Nothing committed.
