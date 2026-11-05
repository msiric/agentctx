# HANDOFF

## State
`unparse(..., *, sort_attributes=False)` (keyword-only, per the user's rule that new optional params go after `*`) implemented in `xmltodict.py` (`_emit` param, forwarded on recursion, sorts the
collected `attrs` dict just before `startElement`). README unparse option list updated. Tests added at the end of
`tests/test_dicttoxml.py`; full suite passes (138). Not committed.

## Decisions
- Sort the final `attrs` dict (after xmlns expansion) so `xmlns*` declarations sort together with normal attributes
  by plain string order of the output name. Simple and deterministic.
- Default off, so existing output is unchanged.

## Failed approaches
None.
