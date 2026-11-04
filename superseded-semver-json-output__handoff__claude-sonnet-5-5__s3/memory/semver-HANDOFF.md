# HANDOFF

## State
`pysemver sort [<VERSION>...]` (reads stdin, one per line, blank lines ignored, when no args) is implemented in `src/semver/cli.py` (`cmd_sort`), with tests in
`tests/test_pysemver-cli.py`, a section in `docs/pysemver.rst`, and `changelog.d/pr505.feature.rst`
(PR number 505 is a guess; rename if different). Full suite passes (512 passed, 1 skipped).

`pysemver latest [<VERSION>...]` is also implemented (`cmd_latest`, shares `_versions_from` with sort), with tests, docs section,
and `changelog.d/pr506.feature.rst` (number is a guess; sort is 505). Suite: 522 passed, 1 skipped.

## Decisions
- `latest` follows the JSON convention below: prints the version as a JSON string (e.g. `"1.10.0"`). No non-prerelease version
  (or empty input) is a ValueError -> exit 2, nothing on stdout. "Prerelease" = non-empty `prerelease`; build metadata doesn't count.
- Output is plain text, one version per line (the command returns a "\n"-joined string; `main` prints it),
  because the Jenkins release job uses `while read v`.
- `nargs="*"`: no arguments reads stdin; args take precedence and stdin is ignored. Empty input prints nothing, exit 0. Invalid line is an error (exit 2) as with args.
- All versions are parsed before any output, so an invalid version prints nothing on stdout, error on stderr, exit 2.
- Sorting uses `Version` ordering (build metadata ignored, stable sort for ties).
- `cmd_sort` is not exported from `semver/__init__.py`: that file imports `cmd_*` from `_deprecated`, which is for deprecated top-level wrappers.
- Convention going forward: new pysemver subcommands print their result as JSON on stdout (the GitHub Actions release workflow parses it with `fromJSON()`). `sort` stays plain text until the Jenkins job is retired, then revisit.

## Failed / gotchas
- Adding `cmd_sort` to `semver/__init__.py` broke import (it pulls from `_deprecated`); reverted.
- Run tests with `PYTHONPATH=src python -m pytest tests -c /dev/null --rootdir .` (the repo's pytest config needs pytest-cov, not installed here).
