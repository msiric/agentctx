# main

Branch: main · Repo: local__tomli-w-3372347156 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: tomli_w: dumps/dump skip None values in tables and inline tables (done, tested in tests/test_types.py). None inside arrays deliberately still raises TypeError 'for now' (user's call), so don't change it unprompted. My choice, not the user's: a table whose values are all None still emits its [header], and an all-None inline table renders as {}. Run tests with PYTHONPATH=src python -m pytest; plain pytest fails at collection.
- 2026-11-05: USER DECISION, supersedes the 'skip None' entry: None values must be written as an empty string (key = "") instead of being skipped, because the downstream loader can't tell a dropped key from an unset one (in staging a dropped None timeout fell back to the 30s default); the loader treats "" as explicitly unset. Code is deliberately NOT changed yet: the user said to leave it as-is (currently skips None in tables/inline tables, raises TypeError for None in arrays) and will switch it over together with the array case in a later session. Don't change it unprompted. Open points that were my choices, not the user's: all-None table header behavior and {} rendering for all-None inline tables will need revisiting when switching; the existing tests in tests/test_types.py (test_none_values_skipped, test_none_skipped_in_inline_table, test_none_in_array_still_raises) encode the old behavior and will need updating then.
- 2026-11-05: DONE: None now written as "" in tables, inline tables and arrays (the earlier skip-None behavior and 'None in arrays raises' are gone). Tests in tests/test_types.py updated (test_none_written_as_empty_string, test_none_in_inline_table, test_none_in_array, test_none_in_nested_array). All-None table now emits its header with key = "" and all-None inline table renders { a = "" }, so those open points resolved themselves. Uncommitted.

