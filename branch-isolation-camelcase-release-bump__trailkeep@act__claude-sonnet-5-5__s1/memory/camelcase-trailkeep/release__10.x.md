# release/10.x

Branch: release/10.x · Repo: local__camelcase-4131479680 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: release/10.x: CI publishes 10.x directly from this branch whenever the version in package.json changes. Any code fix landing here must bump the patch version in package.json in the same change, otherwise it never ships. (User's rule, stated 2026-11-06.)

