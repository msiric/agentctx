# Handoff

## State
`None` is written as an empty string (`key = ""`) everywhere: table values, array-of-tables
entries, inline tables and arrays (nested too). Implemented in `format_literal`
(`src/tomli_w/_writer.py`); the old key-skipping filters were removed. Tests in
`tests/test_none.py` (including a tomllib round trip). Full suite passes (run with
`PYTHONPATH=src`, the package isn't installed in this env).

Also: `format_literal` accepts `pathlib.PurePath` and writes `str(path)` as a basic string.
Tests in `tests/test_types.py` (`test_pathlib*`).

## Decisions
- None -> `""`: the downstream loader can't tell a dropped key from one never set (in staging a
  `None` `timeout` silently fell back to the 30s default); `""` is read as explicitly unset.
  Replaces the earlier "skip None keys" behaviour (user decision).
- A table with only `None` values now renders `[t]` + `k = ""`, no longer an empty table.
- Paths: handled via `PurePath` (lazy import, like `Decimal`); single-line string, never
  multiline. Windows paths keep backslashes, which get escaped by `format_string`.
- Paths as keys are still rejected (`format_key_part` requires `str`); only values were asked.
- Not added to CHANGELOG/README (no unreleased section; left to maintainer).

## Failed approaches
Skipping `None` keys (replaced by `""`, see Decisions); it had to still raise in arrays, which
was then reversed.
