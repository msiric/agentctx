# feature/bearer-token

Branch: feature/bearer-token · Repo: local__bottle-162628494 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: bearer_token on BaseRequest is implemented with tests (test_environ.py) and doctests; uncommitted. My choices: scheme match is case-insensitive, empty/missing token returns None. Commit needs AI disclosure line per AGENTS.md.

