# Private notes: local__semver-994751780

- 2026-11-04: Any new pysemver subcommand must print its result as JSON on stdout, because the release workflow is moving from Jenkins to GitHub Actions and parses output with fromJSON(). Exception: 'sort' stays plain text, one version per line, because the old Jenkins job still calls it until the migration is finished (then it may be revisited).
- 2026-11-04: pysemver latest prints a JSON string (e.g. "1.2.3") per the JSON-output rule for new subcommands; errors (invalid/no stable version) exit 2 with empty stdout
