# Handoff: `dotenv check`

## State
Done. `check` command in `src/dotenv/cli.py`; 5 tests in `tests/test_cli.py`; entry under Unreleased/Added in `CHANGELOG.md`.

## Decisions
- Presence is by key only: `A=` (empty) and bare `A` in .env count as present. Reason: the goal is "key missing", not "value unset".
- Default example path is `.env.example` in the directory of `--file`, as specified.
- Missing keys printed one per line, in example-file order; exit 1 if any, 2 if either file can't be opened (reuses `stream_file`).

## Notes
- Env had no click/dotenv installed; ran with `PYTHONPATH=src`. 20 tests in test_cli.py fail with FileNotFoundError both before and after this change (they spawn the `dotenv` executable, which isn't installed here). Not related.

## Rule (from user)
Anything new in the CLI must never print values, only key names: .env files hold secrets and CI logs are public. `check` complies: it prints only missing key names; errors print only paths.

# Task: `dotenv diff A B`
## State
Done. `diff` in `src/dotenv/cli.py`, 3 tests in `tests/test_cli.py`, CHANGELOG entry.

## Decisions
- Output is key names only (per the rule above): `< KEY` only in A, `> KEY` only in B, `~ KEY` value differs; each group sorted. Never prints values, even for differing keys.
- Exit 1 if any difference, 0 if same, 2 if a file can't be opened (reuses `stream_file`, as `check` does).
- Takes positional A and B; ignores the global `--file`.
- Values compared as parsed: bare `A` (None) differs from `A=` (""). 
- Failed first attempt: tests passed `Path` objects as positional args to `cli.invoke`; click's parser calls `len()` on them and crashes (exit 1, empty output). Tests use `str(path)` for positionals.
- Verified with `PYTHONPATH=src pytest -k "diff or check"`.
