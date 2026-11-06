# next

Branch: next · Repo: local__camelcase-3260039580 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: Do not edit the version in package.json on the next branch. The release job derives the version from changesets and fails if anyone bumps it by hand (stated by user). This overrides the release/10.x rule about bumping the patch version, which applies only to that branch.

