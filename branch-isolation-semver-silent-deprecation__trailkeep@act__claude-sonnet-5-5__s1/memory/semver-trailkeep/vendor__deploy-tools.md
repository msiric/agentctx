# vendor/deploy-tools

Branch: vendor/deploy-tools · Repo: local__semver-1838642911 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: next_version: renamed prerelease_token -> token; old keyword kept as silent keyword-only alias (documented deprecated, NO warnings.warn) because this branch's CI uses -W error. My choice: alias wins if both given.

