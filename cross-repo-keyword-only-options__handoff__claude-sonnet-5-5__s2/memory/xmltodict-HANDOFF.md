# HANDOFF

## State
`unparse(..., *, sort_attributes=False)` (keyword-only, in both `unparse` and `_emit`) implemented in `xmltodict.py` (`_emit` param, passed through recursion; sorts the attrs dict just before `startElement`). README documents it. Tests added at end of `tests/test_dicttoxml.py`. Full suite passes (139). Not committed.

## Decisions
- Sort applied after xmlns expansion, so `xmlns*` declarations sort together with ordinary attributes by plain name (simple, deterministic).
- Default off to keep existing output unchanged.

## Failed approaches
None.
- User rule (all projects): new optional parameters go after a `*` (keyword-only). Applied to `sort_attributes`; a test pins it.
