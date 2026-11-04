# Private notes: local__semver-3535741579

- 2026-11-04: New pysemver subcommands must print their result as JSON on stdout, because the release workflow is moving from Jenkins to GitHub Actions and parses output with fromJSON(). Exception: 'sort' stays plain text (one version per line) until the migration is finished, because the old Jenkins job still calls it.
