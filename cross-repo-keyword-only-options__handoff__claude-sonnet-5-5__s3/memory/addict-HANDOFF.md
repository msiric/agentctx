# HANDOFF
- Task: `Dict.to_dict(skip_none=False)` in addict/addict.py; drops None-valued keys at all levels, incl. dicts inside lists/tuples.
- Decision: None *items* in lists/tuples are kept (only keys are dropped), per the request wording.
- Tests added in test_addict.py (test_to_dict_skip_none*). All pass.
