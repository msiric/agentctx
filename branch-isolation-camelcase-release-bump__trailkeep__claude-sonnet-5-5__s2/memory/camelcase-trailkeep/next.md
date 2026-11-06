# next

Branch: next · Repo: local__camelcase-669050155 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: Do not edit the version in package.json on branch next (user's rule). Reason: the release job derives the version from the changesets and fails if anyone bumps it by hand.

