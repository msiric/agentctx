# HANDOFF

## State
Added `sqlparse.statement_types(sql, encoding=None)` -> `[stmt.get_type() for stmt in parse(sql, encoding)]`
in `sqlparse/__init__.py`. Documented in `docs/source/api.rst` and `CHANGELOG`; test in `tests/test_parse.py`.
Full suite passes (538 passed).

## Decisions
- Thin wrapper over `parse()` so results always match `Statement.get_type()`; no filtering of
  empty/whitespace-only statements (they yield 'UNKNOWN', e.g. `'select 1; ;'`). Callers that
  want to skip those can filter 'UNKNOWN'.
- Returns a list; accepts optional `encoding` like `parse`/`split`.

## Failed approaches
None.
