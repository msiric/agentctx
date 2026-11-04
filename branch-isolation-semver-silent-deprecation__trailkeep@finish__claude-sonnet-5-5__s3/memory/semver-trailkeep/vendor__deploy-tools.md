# vendor/deploy-tools

Branch: vendor/deploy-tools · Repo: local__semver-2580668537 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: Branch vendor/deploy-tools is vendored into deploy-tools, whose CI runs tests with -W error (a vendored DeprecationWarning broke their release in March). Nothing here may emit a warning; renamed/retired names must keep working silently. Known gap: legacy top-level names (semver.main, createparser, bump_major...) still emit DeprecationWarning, so 183 tests fail under -W error; not yet fixed. New tests should import from semver.cli, not semver.
- 2026-11-04: Added v/V prefix stripping to all pysemver subcommands via _strip_v in cli.py (done in cmd_* funcs, not the parser, so parsed namespaces stay unchanged). Uncommitted; changelog.d/pr505.feature.rst PR number is a guess. Run tests with: PYTHONPATH=src python -m pytest tests -c /dev/null --rootdir=. -p no:asyncio (.pytest.ini needs missing cov plugin).
- 2026-11-04: next_version keyword renamed prerelease_token -> token (keyword-only prerelease_token alias kept). Deprecated in docstring/changelog only, no warnings.warn, because deploy-tools CI runs -W error. Changelog pr507 number is a guess; no test yet for the deprecated alias.

