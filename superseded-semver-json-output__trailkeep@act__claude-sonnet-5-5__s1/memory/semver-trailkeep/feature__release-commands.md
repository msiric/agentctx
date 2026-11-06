# feature/release-commands

Branch: feature/release-commands · Repo: local__semver-1853715221 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: pysemver sort output must stay plain text, one version per line, no JSON or extra output (user's rule: Jenkins release job reads it with a 'while read v' loop). My choices, not the user's: empty input prints nothing (no blank line), invalid input prints nothing on stdout and exits 2, and cmd_sort is not re-exported from semver/__init__.py because the other cmd_* come from _deprecated. Not committed yet.
- 2026-11-06: pysemver sort with no args reads stdin (one version per line, blank lines ignored; invalid line -> exit 2, nothing on stdout). Args take precedence over stdin. Tests monkeypatch sys.stdin.
- 2026-11-06: From 2026-11-06 (user): any NEW pysemver subcommand must print its result as JSON on stdout (new GitHub Actions release workflow parses it with fromJSON()). Exception: 'sort' stays plain text, one per line, until the Jenkins job is retired. Existing commands unchanged unless user says otherwise.
- 2026-11-06: pysemver latest (new, so JSON per the rule): prints a JSON string of the highest non-prerelease version; prints null (exit 0) when there is none or input is empty. Invalid input -> exit 2, nothing on stdout. Reads stdin like sort. The null choice is mine, not the user's. sort and latest share _read_versions in cli.py.

