# HANDOFF

## State
Added `skip_none=False` to `Dict.to_dict()` (addict/addict.py). When True, keys whose
value is None are dropped at every level, including dicts inside lists/tuples.
Tests: `test_to_dict_skip_none`, `test_to_dict_skip_none_default_off` in test_addict.py.

## Decisions
- Only dict *keys* are dropped; bare None items inside lists/tuples are kept, since
  removing them would shift indices and the request was about keys.
- Existing behaviour doesn't recurse into lists nested directly in lists; left unchanged.

## Failed approaches
None.
