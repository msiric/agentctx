# Handoff

## State
Implemented on branch `sorted-json` (uncommitted): `JSONStorage.__init__` does `kwargs.setdefault('sort_keys', True)` (`tinydb/storages.py`), docstring updated. Tests added to `tests/test_storages.py`: `test_json_sort_keys_default`, `test_json_sort_keys_disabled`. Full suite passes (230).

The work was earlier backed out because a release was going out and had to contain no storage changes. The user has since asked for it again explicitly; keep it off any release branch until they confirm.

## Known problem: mixed-type keys
Docs like `{"endpoint": "/api/orders", "hits": {200: 1520, 404: 12, "other": 3}}` (ingest job) have a dict mixing int and str keys. `json.dumps(sort_keys=True)` raises `TypeError: '<' not supported between 'str' and 'int'`, so the insert fails. With `sort_keys=False` it works. JSON turns int keys into strings on read regardless.

Options:
1. Default `False`; fixture-writing code passes `sort_keys=True`.
2. Try sorted, fall back to unsorted on `TypeError` (ordering varies silently).
3. Normalize the ingest job's `hits` keys to strings, then the sorted default works. Preferred if the user controls the ingest job.

The ingest job can also pass `sort_keys=False` as a workaround.

## Notes
- `pytest.ini` needs pytest-cov. Run with `-o addopts=""` if the plugin is missing.
