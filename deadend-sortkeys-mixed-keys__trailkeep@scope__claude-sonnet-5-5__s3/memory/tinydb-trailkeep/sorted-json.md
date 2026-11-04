# sorted-json

Branch: sorted-json · Repo: local__tinydb-1185528748 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: JSONStorage sort_keys-by-default backed out (not in today's release). Naive sort_keys=True raises TypeError on mixed int/str keys, e.g. ingest docs {'hits': {200: 1, 'other': 3}}. Options: fallback to unsorted on TypeError, or recursive reorder by str(key). Revisit.
- 2026-11-04: JSONStorage sort_keys=True is now default again (2026-11-04). Mixed int/str key TypeError solved: on TypeError, recursively reorder dicts by str(key) and dump unsorted (_sort_keys_recursive in storages.py). sort_keys=False still disables sorting.

