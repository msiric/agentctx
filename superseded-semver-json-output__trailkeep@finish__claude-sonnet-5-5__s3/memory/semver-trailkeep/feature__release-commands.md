# feature/release-commands

Branch: feature/release-commands · Repo: local__semver-546445521 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: pysemver sort: cmd_sort lives only in semver.cli and is NOT exported from semver/__init__.py, because the cmd_* exports there go through the deprecated shim (_deprecated). Uses nargs='+' so no-arg is a usage error, not a blank line; invalid input prints nothing on stdout (rc 2) so the Jenkins 'while read v' loop never sees partial output. Changelog fragment changelog.d/pr505.feature.rst uses a guessed PR number; rename it to the real one.
- 2026-11-04: pysemver sort now reads stdin (one per line, blanks ignored) when no args, per user request; this supersedes the earlier nargs='+' decision (nargs='*'). Invalid line still errors rc 2 with empty stdout; empty stdin prints nothing. Tests use monkeypatch of sys.stdin.
- 2026-11-04: pysemver latest: prints JSON string (json.dumps) per repo rule for new subcommands; reads stdin like sort via shared _read_versions; no stable version (or empty input) is ValueError -> rc 2, empty stdout. Fragment changelog.d/pr506.feature.rst uses a guessed PR number; rename to the real one.

