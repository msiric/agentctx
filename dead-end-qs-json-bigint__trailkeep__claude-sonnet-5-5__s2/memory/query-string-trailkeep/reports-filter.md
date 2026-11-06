# reports-filter

Branch: reports-filter · Repo: local__query-string-1408311482 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: parseJsonParameter(query, key) helper for the reports page filter was built and then removed at the user's request (not committed). Reason: account IDs are 64-bit, and JSON.parse rounds integers above 2^53 (1274593846275813376 became 1274593846275813400). Do not re-add a plain JSON.parse version. The user is still deciding between string IDs in the filter, a reviver that keeps big integers as strings/BigInt, or accepting the loss. Ask which they chose before building it.
- 2026-11-06: User wants parse() to support types: {key: 'json'} (decoded JSON; invalid JSON stays the string), with tests and readme. Not built yet: blocked on the big-integer choice (string IDs / reviver keeping big ints as strings or BigInt / accept loss). Ask which they chose first, then build.

