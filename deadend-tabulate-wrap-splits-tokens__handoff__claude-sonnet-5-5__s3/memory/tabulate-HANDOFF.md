# HANDOFF

## State
`--wrap WIDTH` for the CLI is implemented (after the release freeze) in `tabulate/cli.py`, with tests in `test/test_cli.py` (`test_inprocess_wrap_option`, `test_inprocess_wrap_invalid_width`). test_cli.py passes (31 tests). Not committed.

## Decisions
- `--wrap` parses as an int >= 1; otherwise error to stderr, exit 2.
- The value is threaded `_main` -> `_open_and_pprint_file` -> `_pprint_file` and passed as `maxcolwidths=wrap`.
- Also passes `break_long_words=False, break_on_hyphens=False`: otherwise textwrap splits ticket IDs (`SUPPORT-2024-118233`) and URLs mid-token, and support copy-pastes those into the tracker. Trade-off: a token longer than WIDTH overflows the column (the tests assert this).
- These kwargs are only passed when `--wrap` is given, so default output is unchanged.

## Notes
- The default rsv reader splits on every whitespace run, so free-text notes need `-s '\t'`, `-r csv` or `-r jsonl` to stay in one cell.
- Example check: `printf 'id\tnote\n1\tescalated as SUPPORT-2024-118233 to the vendor\n' | python -m tabulate -s '\t' -1 --wrap 14` keeps the ID on one line.
- ruff isn't installed in this environment; the code was formatted by hand.
- Possible follow-ups: README/CHANGELOG mention of `--wrap`.
