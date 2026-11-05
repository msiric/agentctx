# Private notes: local__semver-2157759965

- 2026-11-05: User rule: any NEW pysemver subcommand must print its result as JSON on stdout (the GitHub Actions release workflow parses it with fromJSON()). Exception: leave 'sort' as plain text, one per line, unchanged — the old Jenkins job still calls it until the Jenkins-to-Actions migration is finished (then sort may be revisited, only if the user says so). Existing subcommands (bump, check, compare, nextver) were not mentioned; don't change them unasked.
- 2026-11-05: User rule: any NEW pysemver subcommand prints its result as JSON on stdout (GitHub Actions parses with fromJSON()). 'sort' stays plain text until the Jenkins migration is done. Existing bump/check/compare/nextver unchanged unless asked.
