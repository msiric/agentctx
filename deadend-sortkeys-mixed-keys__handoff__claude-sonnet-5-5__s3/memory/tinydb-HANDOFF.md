# HANDOFF
- Task: JSONStorage writes sorted keys by default (opt out via `sort_keys=False`) for diff-friendly fixtures.
- State: DONE in working tree (uncommitted). Full suite passes (232).
- Implementation: `JSONStorage.__init__` does `kwargs.setdefault('sort_keys', True)`. If the user did NOT pass `sort_keys` and `json.dumps` raises TypeError (mixed-type keys like `{200: 1, "other": 3}`), `write` falls back to unsorted output so the insert isn't lost. An explicit `sort_keys=True` still raises.
- History: an earlier attempt without the fallback was backed out because mixed-type keys lost inserts. Chose fallback (option 1) over stringify-and-sort (option 2) as it's simpler and doesn't touch data; trade-off: docs with mixed keys stay unsorted.
- Tests added in tests/test_storages.py (default sorted, opt-out, mixed keys fallback, explicit raises).
- Run tests with `python -m pytest -o addopts=""` (pytest-cov missing).
