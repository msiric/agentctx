# upstream/compare-dict-deprecation

Branch: upstream/compare-dict-deprecation · Repo: local__semver-1592944370 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: Dict arg to Version.compare() now warns DeprecationWarning via warnings.warn (my choice: the deprecated helper wraps whole functions only). Operators (==, <) deliberately not warned - my scope choice, user only asked for compare(). Changelog fragment pr506.deprecation.rst: PR number 506 is my guess; deprecation version number left out as unknown. cli.py/test_pysemver-cli.py/pr505 edits belong to a separate v-prefix task; keep out of this PR.

