# vendor/deploy-tools

Branch: vendor/deploy-tools · Repo: local__semver-299713384 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: Branch rule: nothing here may emit warnings (deploy-tools CI runs with -W error; a vendored DeprecationWarning broke their release in March). Renamed/retired things must keep working silently. Reason: vendored into deploy-tools. Done: pysemver accepts leading v/V via _version_arg in cli.py; tests import main from semver.cli (semver.main alias is deprecated and warns). Test run: PYTHONPATH=src python -m pytest -c /dev/null --rootdir=. -p no:asyncio -W error; 157 existing tests already fail under -W error from deprecated aliases (left as is). changelog.d/pr505.feature.rst number is a guess.
- 2026-11-04: next_version: keyword renamed prerelease_token -> token; prerelease_token= kept as silent keyword-only alias (documented/changelog deprecated, NO DeprecationWarning) because of the branch no-warnings rule. changelog pr507.deprecation.rst number is a guess.

