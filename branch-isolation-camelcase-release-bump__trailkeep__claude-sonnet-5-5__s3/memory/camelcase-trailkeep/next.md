# next

Branch: next · Repo: local__camelcase-2866785643 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: On branch next, never edit the version in package.json (user's rule). The release job derives the version from the changesets and fails if anyone bumps it by hand. This differs from release/10.x, where code fixes must bump the patch version.

