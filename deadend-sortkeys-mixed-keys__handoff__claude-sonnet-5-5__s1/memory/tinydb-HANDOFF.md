# HANDOFF

## State
JSONStorage now writes sorted keys by default; `sort_keys=False` turns it off.
Implemented in tinydb/storages.py, with 3 tests appended to tests/test_storages.py
(default sorted, opt-out, mixed-type keys). Full suite passes (231). Not committed.
Not done: note in docs/usage.rst (an earlier attempt had one).
Run tests with `python -m pytest tests -c /dev/null --rootdir=.` (pytest.ini needs pytest-cov).

## Decisions
- Plain `sort_keys=True` raises TypeError on mixed-type keys, e.g. the ingest docs
  `{"hits": {200: 1520, 404: 12, "other": 3}}`; every insert would fail. So when sorting,
  write() first round-trips (dumps with sort_keys=False, then loads) so keys become strings,
  then dumps with sort_keys=True. Output matches today's JSON, just sorted.
  Cost: double serialize per write.
- Rejected: leaving plain sort_keys=True and having ingest pass sort_keys=False (defeats the default).

## History
An earlier version (plain setdefault, no round-trip) was backed out because a release was
being cut and storage changes were unwanted then. The user has since asked for this again.
