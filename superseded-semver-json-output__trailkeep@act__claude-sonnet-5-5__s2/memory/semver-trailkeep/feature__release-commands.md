# feature/release-commands

Branch: feature/release-commands · Repo: local__semver-3223070901 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: pysemver sort added (cli.py, tests, docs, changelog.d/pr505.feature.rst). My choices: nargs='+' so no-arg is a usage error; any invalid version prints nothing to stdout and exits 2 so the Jenkins 'while read v' loop never sees partial output. PR number 505 in the changelog fragment is a guess: rename to the real one. Nothing committed yet. Tests: .pytest.ini needs the coverage plugin; without it run PYTHONPATH=src python -m pytest tests -c /dev/null --rootdir=.
- 2026-11-06: pysemver sort: user asked (supersedes earlier nargs='+') that no-arg reads stdin, one per line, blanks ignored; nargs='*'. Kept my choice: any invalid version -> nothing on stdout, exit 2. Empty stdin prints nothing, exit 0 (my choice). Args take precedence over stdin.
- 2026-11-06: pysemver latest added (cli.py, tests, docs, changelog.d/pr506.feature.rst - PR number 506 is a guess, rename to the real one). Prints JSON per the repo rule for new subcommands. My choices: output is a JSON string ("1.10.0"); no non-prerelease version or empty input -> prints null, exit 0; build metadata does not count as prerelease; invalid version -> nothing on stdout, exit 2; args take precedence over stdin, nargs='*'. Shared helper _collect_versions also used by sort. Nothing committed.

