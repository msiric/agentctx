# release/10.x

Branch: release/10.x · Repo: local__camelcase-2866785643 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: On release/10.x, CI publishes straight from the branch whenever the version in package.json changes (user's rule). Any code fix landing here must bump the patch version in the same change, otherwise it never ships. Docs-only or no-op changes need no bump. Context: XMLHttpRequest question was answered with no code change (use preserveConsecutiveUppercase: true).
- 2026-11-06: Added '/' to SEPARATORS in index.js (bug: camelCase('aws/region') was unchanged). Bumped version to 10.0.1 per the publish-on-version-change rule. Slash now splits words everywhere, including array-input joins and leading-separator stripping.

