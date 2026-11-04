# Private notes: local__semver-546445521

- 2026-11-04: New pysemver subcommands print their result as JSON on stdout (release workflow is moving from Jenkins to GitHub Actions, which parses output with fromJSON()). Exception: 'sort' stays plain text, one per line, because the old Jenkins job still calls it until migration finishes.
