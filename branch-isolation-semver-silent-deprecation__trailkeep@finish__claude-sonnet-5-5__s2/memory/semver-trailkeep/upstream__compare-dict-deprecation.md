# upstream/compare-dict-deprecation

Branch: upstream/compare-dict-deprecation · Repo: local__semver-420349729 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: compare() dict deprecation: used warnings.warn (stacklevel=2) not the deprecated helper, since the helper wraps whole functions and only one argument type is deprecated. Operators (==, <) with dicts deliberately left silent: _comparator converts before compare(); user only asked about compare(). Changelog fragment pr505.deprecation.rst uses a guessed PR number; rename to the real one.

