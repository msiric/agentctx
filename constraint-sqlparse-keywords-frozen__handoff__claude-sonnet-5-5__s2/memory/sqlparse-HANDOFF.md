# HANDOFF

## State
`sqlformat --check` implemented in `sqlparse/cli.py`, tests added in `tests/test_cli.py`. All CLI tests pass. Not committed.

## Decisions
- `--check` formats in memory, writes nothing, prints each filename whose output differs from input, returns 1 if any differ (or on any error), else 0.
- Multiple files are allowed with `--check` (needed for pre-commit), without `--in-place`.
- `--check` combined with `--in-place` or `-o` is an error (they contradict).
- Works with stdin (`-`), where the printed name is `-`.
- Errors (unreadable file, format failure) also exit 1 and continue to the next file, as before.

## Not done / failed
- `ruff` isn't installed here, so lint wasn't run.
- No CHANGELOG/docs entry yet.

## Standing constraint
- `sqlparse/keywords.py` must stay byte-identical to upstream (weekly merge conflicted there because of an old local tweak, now reverted). Extra keywords go in a module of our own, registered at runtime via `Lexer.add_keywords()`.

## Snowflake keywords (EXCLUDE, MATCH_RECOGNIZE, ASOF, MATCH_CONDITION)
- Added in new `sqlparse/keywords_local.py` (`KEYWORDS_LOCAL`), registered at the end of `Lexer.default_initialization()` in `sqlparse/lexer.py` (2-line change) so it survives `default_initialization()` resets. `keywords.py` untouched, per the standing constraint.
- Test: `test_snowflake_local_keywords` in `tests/test_keywords.py`. Full suite passes.
- All four are plain `Keyword` (no special grouping). `EXCLUDE` is now a keyword everywhere, so a column named `exclude` will be uppercased by `-k upper`.
