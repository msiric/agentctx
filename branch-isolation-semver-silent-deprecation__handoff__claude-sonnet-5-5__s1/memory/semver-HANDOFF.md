# HANDOFF

## State
Every `pysemver` subcommand (bump x5, check, compare, nextver) accepts an optional
leading `v`/`V` on version args. Output has no `v`. Done in `src/semver/cli.py`,
tests in `tests/test_cli_vprefix.py`, changelog `changelog.d/pr505.feature.rst`
(PR number 505 is a guess; rename if different).

## Decisions
- Implemented as an argparse `type=` (`_version_arg`) so all subcommands share it and
  no existing function or signature changed (no deprecations, no warnings).
- Strips one `v`/`V` only when followed by a digit, so `v`, `vv1.2.3`, `v-1.2.3` stay invalid.
- `Version.parse` itself is untouched; the library API does not accept `v`.

## Gotchas
- Tests must import `semver.cli.main`, not `semver.main` (deprecated, warns under `-W error`).
- Running pytest here: `PYTHONPATH=src python -m pytest -W error -p no:asyncio -p no:cov -o addopts="" tests`
  (pytest-asyncio itself emits a DeprecationWarning at configure time; not from this repo).
- Pre-existing, not from this change: with `-W error`, 157 existing tests fail on clean
  main-branch code because they call deprecated module-level functions (e.g. `semver.replace`,
  `semver.main`) outside `pytest.warns`. Not addressed.

---
# Task 2: deprecate dict argument of `Version.compare()` (branch compare-dict-deprecation)

## State
Done: `warnings.warn(DeprecationWarning, stacklevel=2)` in the dict branch of
`Version.compare` (`src/semver/version.py`), docstring `.. deprecated:: 3.0.0`,
fragment `changelog.d/pr506.deprecation.rst` (506 is a guess), tests in
`tests/test_compare_dict_deprecation.py`; `test_direct_compare_with_collections` now uses `pytest.warns`.

## Decisions
- `warnings.warn`, not `_deprecated.deprecated`: that decorator deprecates a whole function
  and cannot target one argument type (and `_deprecated` imports `version`, so circular).
- Operators (`==`, `<`, ...) accept dicts via `_comparator`, which converts to Version before
  calling `compare`, so they do not warn. Left unchanged: the request was about `compare()` only.
- The v-prefix CLI work (Task 1) is uncommitted in the same tree; untouched.

---
# Task 3: rename `next_version(prerelease_token=)` to `token`

## State
Done in `src/semver/version.py`: signature `next_version(part, token="rc", prerelease_token=_UNSET)`.
Old keyword still works, emits DeprecationWarning (stacklevel=2) and overrides `token`.
Docs examples use `token=`; fragment `changelog.d/pr507.deprecation.rst` (507 is a guess);
tests at end of `tests/test_bump.py`.

## Decisions
- `token` stays the 2nd positional param so positional callers are unaffected; the deprecated
  name is a third param. A sentinel (not None) is used because None is a valid token value.
- The rst doctest for the prereleases doc page fails with or without this change (verified via
  stash); not addressed.
