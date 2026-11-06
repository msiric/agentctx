# sorted-json

Branch: sorted-json · Repo: local__tinydb-3518362506 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: JSONStorage now defaults sort_keys=True via kwargs.setdefault (my choice); sort_keys=False opts out. Reason: user commits db.json fixtures and wants stable diffs. Docs in usage.rst and tests in test_storages.py updated.
- 2026-11-06: Sorted-keys change to JSONStorage was backed out at user's request (release cutting, no storage changes). Blocker found: sort_keys=True raises TypeError on mixed int/str keys, e.g. ingest docs {"hits": {200: 1, "other": 3}}. Planned fix when resumed: stringify dict keys recursively before sorting (my recommendation, user hasn't confirmed), plus a test with that shape.
- 2026-11-06: Sorted-keys change re-applied: JSONStorage defaults sort_keys=True; when sorting, dict keys are stringified recursively (json.dumps rules) so mixed int/str keys work (my choice). Tests + usage.rst updated.

