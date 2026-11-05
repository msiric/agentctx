# HANDOFF
Task: add `sort_attributes` (default False) to `unparse`.
- Implemented in `xmltodict.py`: new kwarg on `unparse`, threaded through `_emit` (incl. recursion); attrs dict sorted just before `startElement`, so xmlns-dict-derived attrs are sorted with the rest (by final name).
- Tests appended to `tests/test_dicttoxml.py`.
- README not updated (AGENTS.md: only if public API changes — arguably it does; optional follow-up).
- `sort_attributes` is keyword-only (after `*`) in both `unparse` and `_emit`; user rule: all new optional params go after `*`.
- Not committed.
