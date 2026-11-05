# Handoff

## State
None handling is implemented: a `None` value is written as an empty string
(`key = ""`) in regular tables, AoT tables, inline tables and arrays (nested
and tuples too). Done in one place: `format_literal` returns `'""'` for None;
the earlier skip logic in `gen_table_chunks` / `format_inline_table` was removed.
Tests are in `tests/test_types.py` (`test_none_*`), including a tomllib
round-trip. Run with `PYTHONPATH=src python -m pytest tests` (the package is not
installed; plain `pytest` fails at collection). All tests pass.

## Decisions
- Skipping None keys was replaced: the downstream loader can't tell a dropped
  key from one never set (in staging a None `timeout` fell back to the 30s
  default). Empty string is treated by the loader as explicitly unset.
- Same representation in arrays, so it is consistent everywhere.

## Notes
- CHANGELOG and README not updated.
- Note that None does not round-trip: it reads back as `""`.

## Pathlib support (added later)
`format_literal` now accepts `pathlib.PurePath` (incl. `Path`) values and
writes `str(path)` as a plain basic string (never multiline). Works in tables,
inline tables and arrays. `pathlib` is imported lazily next to `Decimal` to
keep import time low. Path *keys* are still rejected (keys must be `str`).
Test: `test_pathlib_paths` in `tests/test_types.py`. Full suite passes.
