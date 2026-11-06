# vendor/deploy-tools

Branch: vendor/deploy-tools · Repo: local__semver-3175555158 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: User rule for this vendored branch (vendor/deploy-tools): nothing here may emit any warning (deploy-tools CI runs tests with -W error; a vendored DeprecationWarning broke their release in March). If something is renamed or retired, the old spelling must keep working silently, no DeprecationWarning.
- 2026-11-06: Finding (not fixed, out of scope of the v-prefix task): semver.* deprecated shims (semver.main, cmd_*, bump_*, etc. in _deprecated.py) emit DeprecationWarning by design, and ~157 existing tests fail under -W error on baseline. Conflicts with the no-warnings rule; ask user before changing. New CLI tests use semver.cli.main to stay warning-free.
- 2026-11-06: next_version keyword renamed prerelease_token -> token (keyword-only prerelease_token alias kept). Alias is documented as deprecated (docstring + changelog) but emits NO warning, per the branch no-warnings rule. Don't add DeprecationWarning.

