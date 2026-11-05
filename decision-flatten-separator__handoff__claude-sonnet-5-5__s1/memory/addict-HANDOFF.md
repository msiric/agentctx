# HANDOFF

## State
- `Dict.to_dict()` fixed so Dicts inside arbitrarily nested lists/tuples become plain dicts (test `test_to_dict_with_nested_lists`).
- `Dict.flatten(sep='__')` added in `addict/addict.py`, with tests `test_flatten*` in `test_addict.py`. All 140 tests pass.

## Decisions
- `to_dict`: recursive `convert` helper; container type preserved via `type(value)(...)`. Reason: old code only converted direct list items.
- `flatten`: joins nested keys with `__` (not `.`). Reason: the pairs become environment variables and the deploy tooling splits nested names on `__`. Example: `{'db': {'host': 'x'}}` -> `{'db__host': 'x'}`.
- `flatten`: separator is a parameter (`sep`) defaulting to `__`.
- `flatten`: lists/tuples/other non-dict values are leaves, kept as-is (no index in the key), per the task spec.
- `flatten`: non-string keys are converted with `str()`.
- `flatten`: empty nested dicts have no leaves and are omitted. Reason: accessing a missing key on a Dict creates an empty Dict, which would otherwise show up as noise. Easy to change if empty dicts should be kept.
- `flatten` returns a plain `dict` and does not mutate the Dict.

## Failed approaches
None.
