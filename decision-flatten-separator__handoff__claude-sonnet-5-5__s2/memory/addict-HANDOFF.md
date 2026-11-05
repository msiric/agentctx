# HANDOFF
- Task: `Dict.to_dict()` didn't convert Dicts inside nested lists/tuples.
- Fix: `to_dict` in addict/addict.py now uses a recursive `unwrap` helper (handles list/tuple at any depth; converts any `Dict` subclass).
- Test: `test_to_dict_with_nested_lists` in test_addict.py.
- Failed approaches: none.

## `Dict.flatten(separator='__')` (done)
- Purpose: export nested service config as flat key/value pairs (env vars on deploy side; tooling splits on `__`).
- Returns a plain dict; one entry per leaf; keys joined with `__` by default (overridable via `separator`). Example: `{'db': {'host': 'x'}}` -> `{'db__host': 'x'}`.
- Decisions: lists/tuples are leaves, returned unchanged (even if they contain Dicts), per the ticket. Non-string keys are `str()`-ed. Keys already containing `__` are NOT escaped, so collisions/ambiguity are possible (open question, unresolved). Empty nested dicts produce no entry.
- Tests: `test_flatten*` in test_addict.py (138 pass).
- Failed approaches: none.
