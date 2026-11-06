# HANDOFF

## State
`sqlformat --check` implemented in `sqlparse/cli.py`, with tests in `tests/test_cli.py` and a CHANGELOG entry. Full suite passes. Not committed. ruff was not available to run.

## Decisions
- `--check` formats in memory, writes nothing, prints each filename whose output differs from input, exits 1 if any differ (or on any error), else 0.
- Allowed with multiple files without `--in-place` (needed for pre-commit).
- Rejected with `--in-place` or `-o` (contradicts "write nothing").
- Works with stdin (`-`); the name printed is `-`.
- Comparison uses text read with universal newlines, so CRLF files compare as LF-normalized.

- Snowflake keywords EXCLUDE, MATCH_RECOGNIZE, ASOF, MATCH_CONDITION live in `sqlparse/local_keywords.py` and are added in `Lexer.default_initialization()` (lexer.py), so `keywords.py` is untouched. Tests in `tests/test_parse.py`. Uncommitted.

## Failed approaches
- Registering the keywords at `import sqlparse` time via a `register()` call: other tests call `default_initialization()`/`clear()`, wiping the registration, so 4 tests failed in the full suite. Hooking into `default_initialization()` fixes that.

## Standing constraint
`sqlparse/keywords.py` must stay byte-identical to upstream so the weekly upstream merge stays clean (an old local tweak there caused repeated conflicts and has been reverted). Extra keywords must be registered at runtime via `Lexer.add_keywords()` from a separate module of our own, never by editing `keywords.py`.
