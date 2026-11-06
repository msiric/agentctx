# HANDOFF

## State
Added `sqlparse.statement_types(sql, encoding=None)` in `sqlparse/__init__.py`:
`[s.get_type() for s in parse(sql, encoding)]`. Documented in
`docs/source/api.rst` and CHANGELOG; test in `tests/test_parse.py`.
Full suite passes (538 passed). Not committed.

## Decisions
- Built on `parse()` (not `split()`) so results match `get_type()` exactly.
- Optional `encoding` arg mirrors `parse`/`split`.
- Unknown statements yield `'UNKNOWN'` (existing get_type behaviour).

## Notes
- `ruff` isn't installed in this env; lint not run.
