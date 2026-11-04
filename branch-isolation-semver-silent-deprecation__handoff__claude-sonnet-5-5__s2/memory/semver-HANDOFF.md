# HANDOFF

## State
`pysemver` subcommands (bump, check, compare, nextver) accept one optional leading `v`/`V` on
version args; output has no `v`. Implemented via `_strip_v` in `src/semver/cli.py`; tests at the
end of `tests/test_pysemver-cli.py`; changelog fragment `changelog.d/pr505.feature.rst` (PR number is a guess).

## Decisions
- Stripping is done in the `cmd_*` functions, not in argparse `type=`: existing tests compare the parsed
  Namespace against raw strings.
- Only one `v` is stripped, so `vv1.2.3` stays invalid.
- New tests call `semver.cli.main`, not `semver.main`, because the latter is a deprecated wrapper that warns.

## Known issue (not touched)
Under `-W error` the existing suite has ~157 failures: tests call deprecated top-level functions
(`semver.main`, `semver.compare`, `semver.match`, ...), which emit Deprecation warnings by design
(`src/semver/_deprecated.py`). Pre-existing on this branch; conflicts with the "no warnings" rule. Needs a decision.
Also: the pytest-asyncio plugin warns at configure time; run with `-p no:asyncio -o addopts=""` locally.

## Task 2: deprecate dict in `Version.compare()` (branch compare-dict-deprecation)
Done: `Version.compare` emits `DeprecationWarning` (`warnings.warn`, stacklevel=2) when `other` is a dict;
docstring has `.. deprecated::`; fragment `changelog.d/pr506.deprecation.rst` (PR number is a guess);
tests at the end of `tests/test_compare.py`.
- `warnings.warn` rather than the `deprecated` helper: the helper deprecates a whole function, and
  here only one argument type is deprecated.
- Operators (`==`, `<`, ...) convert dicts in `_comparator` before calling `compare`, so they do not warn;
  not in scope (only `compare()` was requested). Test pins this.
- The `.. deprecated:: 3.0.0` version number is a guess; check against the release plan.
- The uncommitted `_strip_v` work above is unrelated to this task and was left untouched.

## Task 3: rename `next_version(prerelease_token=)` to `token`
Done: `token` is the 2nd positional/keyword param; `prerelease_token` is a keyword-only deprecated alias
(`DeprecationWarning`, stacklevel=2; TypeError if combined with a non-default `token`). Docs example updated,
tests at end of `tests/test_bump.py`, fragment `changelog.d/pr507.deprecation.rst` (PR number and `3.0.0` are guesses).
- Known gap: `token="rc", prerelease_token=...` is not detected as a conflict (`rc` is the default).
- Unrelated uncommitted work from tasks 1-2 left untouched.
