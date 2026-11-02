# HANDOFF

## State
Added `dotenv check [--example PATH]` in `src/dotenv/cli.py`: lists keys in the example file that are
missing from the .env file (one per line, example order); exit 1 if any missing, 2 if either file
can't be opened. Tests in `tests/test_cli.py` (`test_check_*`), CHANGELOG entry added. README not updated.

## Decisions
- Default example is `.env.example` in the same directory as the `--file` .env (per request: "next to it").
- A key counts as present in .env if it appears at all, including bare keys (`FOO` with no `=`) and empty values.
- Bare keys in the example count as required keys.
- Unreadable files reuse `stream_file` (exit 2), consistent with `list`/`get`.

## Notes
- Run tests with `PYTHONPATH=src` (package isn't installed here). ~20 `test_run_*` tests in test_cli.py
  fail in this environment because they shell out to a `dotenv` executable that isn't installed;
  they fail identically without my change.
- First attempt at `test_check_missing_env_file` failed because the `dotenv_path` fixture creates the file; fixed by unlinking.

## Rule
New CLI commands must never print values, only key names (CI logs are public). `check` complies and
`test_check_never_prints_values` guards it.

## `dotenv diff A B` (added after `check`)
`diff` in `src/dotenv/cli.py`: positional paths A and B (does not use `--file`). Prints `< KEY` (only in A),
`> KEY` (only in B), `~ KEY` (value differs), each group sorted; exit 0 same, 1 differ, 2 unreadable file.
- Key names only, never values (follows the Rule above); tests `test_diff_*` guard it.
- Bare key (`FOO`, value None) vs `FOO=` (empty string) counts as different.
- Ordering is sorted rather than file order since the files may order keys differently.
- CHANGELOG updated; README not.
