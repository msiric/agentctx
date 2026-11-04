# feature/release-commands

Branch: feature/release-commands · Repo: local__semver-762097513 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: pysemver sort added (cli.py cmd_sort, docs, tests). Decisions: plain text one-per-line because Jenkins release job reads it with 'while read v'; invalid input prints nothing to stdout, error on stderr, rc 2, so the loop never sees partial output. Changelog fragment changelog.d/pr505.feature.rst uses a guessed PR number: rename to the real one. Nothing committed yet. Run tests with PYTHONPATH=src and -c /dev/null (.pytest.ini coverage flags fail here).
- 2026-11-04: sort with no args reads stdin (one per line, blanks ignored); invalid line still rc 2, nothing on stdout, same as args. nargs changed + to *.
- 2026-11-04: Rule from user (2026-11-04): Jenkins->GitHub Actions migration; workflow parses output with fromJSON(). Any NEW pysemver subcommand must print its result as JSON on stdout. Leave 'sort' as plain text one-per-line: old Jenkins job still calls it until migration finishes.
- 2026-11-04: pysemver latest added (cli.py cmd_latest, docs, tests, changelog.d/pr506.feature.rst - guessed PR number, rename). Prints JSON string e.g. "1.10.0" per the fromJSON rule; no stable version or invalid input -> nothing on stdout, rc 2. Shares _read_versions (args or stdin) with sort.

