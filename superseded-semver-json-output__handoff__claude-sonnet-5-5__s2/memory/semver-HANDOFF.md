# HANDOFF

## State
`pysemver sort [VERSION...]` added (src/semver/cli.py `cmd_sort`), with tests in
tests/test_sort.py, docs in docs/pysemver.rst, changelog.d/505.feature.rst
(505 is a guessed number; rename to the real PR/issue number).

## Update: `pysemver latest [VERSION...]`
Added `cmd_latest` (cli.py), tests/test_latest.py, docs section, changelog.d/506.feature.rst
(506 also a guessed number). Follows the JSON convention below: prints a JSON string
(`"1.10.0"`). Same args/stdin handling as sort. No stable version (none given, or all
prereleases) -> ValueError, exit 2, nothing on stdout (chosen over printing `null` so
callers fail loudly). Build metadata is preserved in output; ordering via Version `max`.

## Decisions
- Output is plain `"\n".join`, one version per line, for Jenkins `while read v`.
- No args: read stdin, one version per line, blank lines skipped (args win if given).
- Zero versions (empty stdin too): prints nothing, exit 0 (returns None; `nargs="*"`), so no blank line.
- Invalid version (arg or stdin): exit 2, nothing on stdout (all parsed before printing).
- Not re-exported from `semver/__init__` (those cmd_* names are deprecated shims).

## Failed approaches
- `pytest` with the repo's .pytest.ini fails here (pytest-cov options not installed);
  ran with `-c /dev/null --rootdir=.` instead.

## Conventions for future subcommands
- New pysemver subcommands print their result as JSON on stdout: the release
  workflow is moving from Jenkins to GitHub Actions, which parses output with
  `fromJSON()`.
- `sort` is deliberately left as plain text (one version per line): the old
  Jenkins job still calls it until the migration finishes. Don't convert it
  until then.
