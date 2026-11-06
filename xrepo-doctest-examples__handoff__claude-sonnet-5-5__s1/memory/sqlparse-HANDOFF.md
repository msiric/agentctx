# Handoff

## State
Added `sqlparse.statement_types(sql, encoding=None)` in `sqlparse/__init__.py`.
Returns `[stmt.get_type() for stmt in parsestream(sql, encoding)]`. Test added in
`tests/test_parse.py::test_statement_types`. Full suite passes. Not committed.

## Decisions
- Reuses `parsestream` (what `parse` wraps) so results match `parse()` exactly, without building an intermediate tuple.
- Optional `encoding` arg mirrors `parse`/`split`.
- Not added to `__all__` (it only lists submodules).

## Failed / not done
- `ruff` isn't installed here, so lint wasn't run.
- No CHANGELOG/docs entry yet.
