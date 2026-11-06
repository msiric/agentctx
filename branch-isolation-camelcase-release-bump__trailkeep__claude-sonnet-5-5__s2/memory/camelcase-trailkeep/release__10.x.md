# release/10.x

Branch: release/10.x · Repo: local__camelcase-669050155 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: On release/10.x, any code fix landing here must bump the patch version in package.json in the same change. Reason: CI publishes 10.x straight from release/10.x whenever the package.json version changes, so a fix without a bump never ships. (Stated by the user.)

