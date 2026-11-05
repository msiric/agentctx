# Handoff

## State
Fixed `Dict.to_dict()` so Dicts nested at any depth inside lists/tuples are converted to plain dicts. Regression test `test_to_dict_with_nested_sequences` added in `test_addict.py`. All tests pass (130). Not committed.

## Decisions
- Replaced the one-level list/tuple handling with a recursive classmethod `_unwrap` in `addict/addict.py`. Reason: the old code only converted direct list items, so `[[{...}]]` was left as a Dict.
- Kept `type(value)(...)` to preserve list/tuple type (existing behavior; unchanged).

## Failed approaches
None.

## Done: `Dict.flatten(separator='__')`
- Implemented in `addict/addict.py`; tests `test_flatten*` in `test_addict.py`. All tests pass (138). Not committed.
- Default separator is `__` (not `.`): output feeds env-var deploy tooling that splits nested names on a double underscore. Example: `{'db': {'host': 'x'}}` -> `{'db__host': 'x'}`.
- Lists/tuples are leaves, returned unchanged except Dicts inside are converted to plain dicts via `_unwrap`.
- Empty nested dict is kept as a leaf (`{'e': {}}` -> `{'e': {}}`) so keys aren't silently dropped. Non-str keys are stringified.
- Test pitfall: don't use `items` as an attribute name in tests (read-only dict method).
