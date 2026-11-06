# HANDOFF

## State
`sqlformat --check` implemented in `sqlparse/cli.py`, with tests in `tests/test_cli.py`.
Formats in memory, writes nothing, prints names of files that would change, exit 1 if any (or on error), else 0.

## Decisions
- Multiple files allowed with `--check` (needed for pre-commit); otherwise still require `--in-place`.
- `--check` with `--in-place` or `-o` is an error (contradicts "write nothing").
- Comparison is against exactly what normal formatting would output, so a file is "changed" iff `--in-place` would modify it.
  Note: formatter drops the trailing newline (e.g. with `-r`), so files ending in "\n" are flagged under such options.
  Not altered: out of scope and would change formatting output.

## Standing rule
- `sqlparse/keywords.py` must stay byte-identical to upstream so the weekly upstream merge stays clean (a local tweak there caused repeated conflicts). Extra keywords are registered at runtime via `Lexer.add_keywords()` from a separate module of our own.

## Snowflake keywords (EXCLUDE, MATCH_RECOGNIZE, ASOF, MATCH_CONDITION)
- Added in `sqlparse/extra_keywords.py`, registered via `extra_keywords.register()` in `sqlparse/__init__.py` (keywords.py untouched, per standing rule). Test: `test_local_snowflake_keywords` in tests/test_regressions.py.
- `register()` also wraps `Lexer.default_initialization` so the keywords survive resets (tests/test_parse.py resets the singleton; without the wrapper the new test failed in the full suite but passed alone). Failed first attempt: plain add_keywords only.
- ruff not installed in env, so lint not run.
