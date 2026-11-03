# sorted-json

Branch: sorted-json · Repo: local__tinydb-4034376436 · Kind: branch · Created: 2026-11-02

## Decisions and dead ends

- 2026-11-02: Reverted sort_keys=True default for JSONStorage (user wants no storage changes in today's release). Why it failed: json.dumps(sort_keys=True) raises TypeError on mixed int/str dict keys, e.g. ingest docs {'hits': {200: 1520, 'other': 3}}. Preferred retry: stringify keys before sorting in write(), plus regression test with that doc.
- 2026-11-02: Re-landed sort_keys=True default in JSONStorage (user asked again). Mixed int/str keys handled by _stringify_keys in write(); regression test test_json_sort_keys_mixed_key_types.

