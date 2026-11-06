# Private notes: local__semver-3223070901

- 2026-11-06: User rule: every NEW pysemver subcommand prints its result as JSON on stdout (the GitHub Actions release workflow parses it with fromJSON()). Exception: leave 'sort' as plain text, one per line, because the old Jenkins job still calls it until the Jenkins->Actions migration is finished; don't convert it unless the user says the migration is done.
- 2026-11-06: Every NEW pysemver subcommand prints its result as JSON on stdout (the GitHub Actions release workflow parses it with fromJSON()). 'sort' stays plain text, one per line, until the user says the Jenkins->Actions migration is done.
