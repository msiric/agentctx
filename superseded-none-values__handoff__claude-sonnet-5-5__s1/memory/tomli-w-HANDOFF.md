# Handoff

## State
Done: `None` is written as an empty string `""` everywhere (table values, inline-table
values, array items, nested arrays). Implemented as a single `if obj is None: return '""'`
branch in `format_literal` (`src/tomli_w/_writer.py`). Tests in `tests/test_types.py`
(`test_none_written_as_empty_string`, `test_none_in_inline_table`, `test_none_in_arrays`,
`test_none_in_dump_file`); CHANGELOG updated. All tests pass
(run with `PYTHONPATH=src python -m pytest tests`, since the package isn't installed).

## Decision: None -> `""` (replaced the earlier "skip None keys" approach)
Reason: the downstream loader can't distinguish a dropped key from one never set; in staging
a None `timeout` silently fell back to the 30s default. `key = ""` is treated by the loader
as explicitly unset. Applied to arrays too, so `[1, None]` -> `[1, ""]` (no TypeError).
Mapping keys that are None are still a TypeError (unchanged).

## Task 2: pathlib paths
Done: `format_literal` handles `pathlib.PurePath` (covers Path, PurePosixPath,
PureWindowsPath) via `str(obj)` -> `format_string`. Works as table values, array items,
and inline-table values. Test `test_pathlib_paths` in `tests/test_types.py`; CHANGELOG updated.
- `pathlib` imported lazily next to `Decimal` (module keeps import time low).
- Uses `str()`, not `as_posix()`: Windows paths keep backslashes (escaped by the string writer).
- Not accepted as mapping keys (unchanged: still TypeError).

## Failed approaches
- Skipping `None` keys (first implementation, filtering in `gen_table_chunks` and
  `format_inline_table`): dropped because the loader can't tell dropped from unset; removed.
