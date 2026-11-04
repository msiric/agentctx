# vendor/deploy-tools

Branch: vendor/deploy-tools · Repo: local__semver-2954968033 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: vendor/deploy-tools: nothing on this branch may emit a warning (deploy-tools CI runs the suite with -W error; in March a vendored DeprecationWarning broke their release pipeline for a day). If something is renamed or retired, the old spelling must keep working silently. Open item: deprecated shims (semver.main, semver.replace, semver.cmd_*, semver.createparser) still warn and 157 existing tests fail under -W error; not yet made silent. Done: CLI accepts leading v/V on versions (src/semver/cli.py _strip_v).

