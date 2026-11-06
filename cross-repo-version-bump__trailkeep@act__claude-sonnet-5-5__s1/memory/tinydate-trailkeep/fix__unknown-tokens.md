# fix/unknown-tokens

Branch: fix/unknown-tokens · Repo: local__tinydate-4124311425 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: Unknown tokens like {foo} are now emitted literally (src/index.js) instead of throwing; I (the assistant) replaced the old test expecting 'MAP[key] is not a function' with literal-output tests. Version bumped to 1.3.1 (patch); changes are uncommitted.

