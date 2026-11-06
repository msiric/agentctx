# release/10.x

Branch: release/10.x · Repo: local__camelcase-3260039580 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: On release/10.x, CI publishes straight from the branch whenever the version in package.json changes. Any code fix landing here must bump the patch version in the same change, otherwise it never ships (stated by user).
- 2026-11-06: Added '/' to SEPARATORS in index.js (aws/region -> awsRegion); in regex v-mode '/' must be escaped inside a class. Bumped to 10.0.1 per the publish rule. Working tree already had uncommitted unrelated changes (capitalizeAfterNumber default false) that I left untouched.

