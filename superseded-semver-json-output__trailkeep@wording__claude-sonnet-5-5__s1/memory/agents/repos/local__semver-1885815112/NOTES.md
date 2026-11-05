# Private notes: local__semver-1885815112

- 2026-11-05: pysemver stdout output is read by release scripts (Jenkins 'while read v'): keep command output plain text, one item per line, no JSON or extras.
- 2026-11-05: User rule (2026-11-05): release workflow is moving from Jenkins to GitHub Actions, which parses pysemver output with fromJSON(). Every NEW pysemver subcommand must print its result as JSON on stdout. Exception: 'sort' stays plain text, one per line, because the old Jenkins job still calls it until the migration is finished; do not convert it until the user says so. This supersedes the earlier plain-text-only note for new commands.
