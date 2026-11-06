# upstream/compare-dict-deprecation

Branch: upstream/compare-dict-deprecation · Repo: local__semver-1838642911 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: compare-dict deprecation: used warnings.warn (stacklevel=2) in Version.compare, not the deprecated helper, because it wraps whole functions and _deprecated.py imports version.py (circular). My choice: ==/< operators with dicts stay silent (they convert before compare). Changelog fragment changelog.d/compare-dict.deprecation.rst needs renaming to prNNN.deprecation.rst once the PR number exists.

