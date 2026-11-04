# Handoff

## State
`dotenv get KEY --default VALUE` implemented in `src/dotenv/cli.py`; tests added in `tests/test_cli.py`. Done.

## Decisions
- Default applies when the key is missing or bare (no `=`). Empty-string values print empty, not the default.
- `--default ""` is honored (checked `is None`, not truthiness).
- File-open errors still exit 2; the default doesn't mask them.

## Gotchas
- A different `dotenv` is installed in site-packages; run tests with `PYTHONPATH=src python -m pytest tests`. Without it, new tests fail with "no such option".
- 5 tests fail before and after this change (`*expands_user*`), unrelated.
