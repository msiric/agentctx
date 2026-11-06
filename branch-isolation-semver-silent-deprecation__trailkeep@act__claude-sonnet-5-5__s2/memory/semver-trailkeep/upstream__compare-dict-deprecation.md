# upstream/compare-dict-deprecation

Branch: upstream/compare-dict-deprecation · Repo: local__semver-3175555158 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: My choices (not user rules): Version.compare dict deprecation uses warnings.warn (stacklevel=2), not the deprecated helper, because the helper warns on every call and only dict args are deprecated. Comparison operators (==, <) with a dict deliberately do not warn; the user scoped this to compare() only. Unconfirmed guesses: changelog fragment named pr506.deprecation.rst (PR number guessed) and docstring says 'deprecated:: 3.0.0'. Uncommitted v-prefix CLI work (pr505) shares this working tree; keep it out of this PR's commit.

