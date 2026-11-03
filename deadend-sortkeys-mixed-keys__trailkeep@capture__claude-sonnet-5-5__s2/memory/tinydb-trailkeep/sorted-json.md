# sorted-json

Branch: sorted-json · Repo: local__tinydb-1620123710 · Kind: branch · Created: 2026-11-03

## Decisions and dead ends

- 2026-11-03: Sorted-keys default for JSONStorage was implemented then reverted (release freeze, user will return). Learned: json.dumps(sort_keys=True) raises TypeError on mixed int/str keys (ingest docs like hits={200:..,'other':..}); fix was custom recursive sort (numbers first, then str) with sort_keys popped from kwargs. Int keys read back as strings.
- 2026-11-03: JSONStorage sorted-keys re-implemented: custom _sort_keys in storages.py; numeric-looking string keys sort numerically so doc IDs keep order ('2' before '10') on reload; plain lexicographic sort would reorder db.all().

