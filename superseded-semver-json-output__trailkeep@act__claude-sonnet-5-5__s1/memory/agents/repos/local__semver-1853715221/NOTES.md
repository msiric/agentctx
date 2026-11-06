# Private notes: local__semver-1853715221

- 2026-11-06: New pysemver subcommands print their result as JSON on stdout (GitHub Actions release workflow parses it with fromJSON()). Exception: 'sort' stays plain text, one version per line, until the Jenkins job that calls it is retired. Existing commands are unchanged unless the user says otherwise.
