# upstream/compare-dict-deprecation

Branch: upstream/compare-dict-deprecation · Repo: local__semver-299713384 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: Dict arg to Version.compare deprecated via warnings.warn (not the deprecated helper): helper wraps whole functions and _deprecated.py imports version.py (circular). Fragment: changelog.d/pr506.deprecation.rst (PR number is a guess).

