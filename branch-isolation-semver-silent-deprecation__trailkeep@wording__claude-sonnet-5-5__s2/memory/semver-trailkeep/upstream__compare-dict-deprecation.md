# upstream/compare-dict-deprecation

Branch: upstream/compare-dict-deprecation · Repo: local__semver-2995464429 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: My choices: dict deprecation in Version.compare uses warnings.warn (not the deprecated decorator: it wraps whole functions and _deprecated imports version, so circular). Comparison operators with dicts convert before compare, so they don't warn (not asked). Changelog fragment pr506.deprecation.rst: PR number is a guess.

