# HANDOFF
Task: `skip_none` flag on `Dict.to_dict()` (addict/addict.py), default False.
- Drops None-valued keys at every level, including dicts inside lists/tuples. None *list items* are kept (only keys are skipped).
- Refactored into helper `_to_plain`, which also now recurses into lists nested in lists (previously not converted).
- Tests: test_to_dict_skip_none*, in test_addict.py. All pass.
