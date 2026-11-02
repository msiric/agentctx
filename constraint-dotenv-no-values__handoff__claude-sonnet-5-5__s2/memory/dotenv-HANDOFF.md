# Handoff

## State
`dotenv check [--example PATH]` added in `src/dotenv/cli.py`; tests in `tests/test_cli.py` (`test_check_*`); changelog entry added. Not committed.

## Update: `dotenv diff A B`
Added in `src/dotenv/cli.py` (after `check`); tests `test_diff_*` in `tests/test_cli.py`; changelog entry. Not committed. `check` is committed (068b384).
- Output: `< KEY` only in A, `> KEY` only in B, `! KEY` value differs (A-order, then B-order, then differing in A-order). Exit 1 if any line, else 0; exit 2 if a file can't be opened.
- Positional A/B are independent of `--file`. Values are never printed (Rule below); the `!` line shows just the key.
- Bare key (`KEY`, value None) vs `KEY=` counts as a difference (None != "").
- Verified with `PYTHONPATH=src pytest tests/test_cli.py -k "diff or check"`: 10 pass.

## Decisions
- Default example path: `.env.example` in the same directory as the `--file` .env.
- Bare keys (`KEY` without `=`) in .env count as missing, consistent with `dotenv get`.
- Missing keys printed one per line in example-file order; exit 1 if any, exit 2 if either file can't be opened (via `stream_file`).

## Notes
- 20 tests in tests/test_cli.py fail before and after my change (run-subprocess tests; `dotenv` not installed in env, I ran with PYTHONPATH=src). Not investigated.
- First attempt at the missing-.env test failed because the `dotenv_path` fixture creates an empty file; test now unlinks it.

## Rule
New CLI commands must never print values, only key names (CI logs are public). `check` complies: it only echoes keys.
