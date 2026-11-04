# Handoff

## State
`pysemver sort <VERSION>...` is implemented in `src/semver/cli.py` (`cmd_sort`), with tests in
`tests/test_pysemver-cli_sort.py`, a section in `docs/pysemver.rst`, and `changelog.d/pr505.feature.rst`
(PR number is a guess; rename if different). Full suite passes (512 passed, 1 skipped).

## Decisions
- Output is plain text, one version per line, via the existing `main()` print of the returned string.
  The Jenkins job uses `while read v`, so there is no JSON or extra output.
- `nargs="*"`: with no arguments, versions are read from stdin (one per line, stripped, blanks ignored).
  Arguments take precedence over stdin. Empty stdin prints nothing, exit 0. Invalid stdin line is still exit 2.
- Any invalid version fails the whole command (exit 2, nothing on stdout) rather than printing a partial list.
- Versions print as given (`str(Version)`); sorting uses `Version` ordering, which ignores build metadata (ties keep input order).
- `cmd_sort` is NOT exported from `semver/__init__.py`. That file re-exports the deprecated
  `cmd_*` wrappers from `_deprecated.py`; a new command should not be born deprecated.
- Convention for NEW subcommands: print the result as JSON on stdout (the GitHub Actions release workflow
  parses it with `fromJSON()`). `sort` is deliberately left as plain text because the old Jenkins job still
  calls it; revisit once the Jenkins -> GitHub Actions migration is finished.

## `latest` (added after sort)
- `pysemver latest [<VERSION>...]` -> `cmd_latest` in `cli.py`, tests in `tests/test_pysemver-cli_latest.py`,
  docs section, `changelog.d/pr506.feature.rst` (PR number guessed).
- Follows the new-subcommand convention: prints JSON (`json.dumps`), i.e. `"1.10.0"` or `null`.
- No stable version (only prereleases, or empty input) -> `null`, exit 0, so `fromJSON()` always gets valid JSON.
  Chosen over an error exit; easy to change if the workflow prefers failing.
- "Not a prerelease" = `not v.prerelease`; build metadata is ignored in comparison but kept in output.
- Same stdin/argument rules and invalid-input behaviour (exit 2, empty stdout) as `sort`. Full suite: 525 passed, 1 skipped.

## Failed
- Adding `cmd_sort` to `semver/__init__.py` broke the import (it pulls the names from `_deprecated`). Reverted.
- Plain `pytest` fails here because `.pytest.ini` needs pytest-cov; I ran with `-c /dev/null` and `PYTHONPATH=src`.
