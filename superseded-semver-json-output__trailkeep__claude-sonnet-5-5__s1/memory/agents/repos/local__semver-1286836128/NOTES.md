# Private notes: local__semver-1286836128

- 2026-11-04: New pysemver subcommands must print their result as JSON on stdout (the GitHub Actions release workflow parses it with fromJSON(), replacing Jenkins). Exception: 'sort' stays plain text, one version per line, because the old Jenkins job still calls it until the migration is finished; revisit then.
