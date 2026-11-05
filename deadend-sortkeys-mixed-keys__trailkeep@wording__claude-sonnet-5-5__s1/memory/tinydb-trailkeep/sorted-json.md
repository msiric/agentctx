# sorted-json

Branch: sorted-json · Repo: local__tinydb-3166529027 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: Task: make JSONStorage write sorted keys by default (opt-out via sort_keys=False). Implemented, then reverted at user's request (release cut, no storage changes). Blocker found: json.dumps(sort_keys=True) raises TypeError on mixed int/str keys, e.g. ingest docs {'hits': {200: 1520, 'other': 3}}. Unimplemented plan (my recommendation): stringify then sort keys in a pre-pass in JSONStorage.write, plus a test with that document shape. Alternatives: fallback to unsorted on TypeError, or keep default off and have fixtures opt in. Note: pytest.ini --cov flags fail here; run with -c /dev/null --rootdir=. tests.
- 2026-11-05: Re-implemented sorted-keys default in JSONStorage (tinydb/storages.py) using the recorded plan: _sort_keys pre-pass stringifies then sorts keys so mixed int/str keys don't raise TypeError; sort_keys=False opts out. Tests added in tests/test_storages.py; full suite passes (231).

