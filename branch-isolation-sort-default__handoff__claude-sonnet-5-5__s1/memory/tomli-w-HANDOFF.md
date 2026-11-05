# HANDOFF

Branch: `acme` (the build shipped to Acme). Main branch: `main`.

## Current state
- On `main`: `sort_keys` implemented (keyword-only, default False) in `dump`/`dumps`, plumbed via `Context`; helper `mapping_items` used by `gen_table_chunks` and `format_inline_table`. Tests added at the end of tests/test_valid.py. Full suite passes (run with `PYTHONPATH=src`; package isn't installed in this env). Committed on `main` as 8b685db (HANDOFF.md itself deliberately left untracked).
- On `acme`: DONE. Cherry-picked 8b685db as f597146, then flipped default to True in a separate commit (HEAD). Suite passes (273 passed, 2 xfailed).
- Order-dependent existing tests (test_style: newline_before_table, tricky_keys, array_of_long_tables, non_trivial_nesting; test_types: decimal) pin `sort_keys=False` on acme; expect small conflicts there on future syncs. Two of those lines exceed the formatter's line length; run the formatter if pre-commit complains.
- Remaining: warn Acme reviewers that output reorders once; not pushed.
- Plan (owned by the user): add a `sort_keys` option on `main` first, then bring it to `acme`.
  On `acme` it must default to ON, because Acme's tooling calls plain `dumps()` and their call sites can't change.

## Findings (src/tomli_w/_writer.py)
- Insertion order is preserved within each kind of key: inline tables (`format_inline_table`, iterates `obj.items()`), scalars among themselves, sub-tables among themselves, and entries of an expanded array of tables.
- It is NOT preserved across kinds. `gen_table_chunks` splits keys into `literals` and `tables`, writes all literals first, then all tables.
  - Scalars move ahead of sub-tables (required by TOML).
  - An array of tables is inline (among the literals) if every entry fits within MAX_LINE_LENGTH (100) via `is_suitable_inline_table`, otherwise it becomes `[[x]]` sections after all literals. A change in value length can move the whole block.
- Output is deterministic for identical input. The churn Acme sees comes from how our side builds the dicts (order of construction) plus the points above.

## Decisions and reasons
- Default flip on `acme` goes in its own commit on top of the cherry-picked upstream patch, so later syncs with `main` don't conflict on the `dump`/`dumps` signatures.
- Add a test on `acme` asserting plain `dumps()` sorts, so a sync can't silently undo the default.

## Design notes for the `sort_keys` patch
- Sort keys at both `gen_table_chunks` (table.items()) and `format_inline_table` (obj.items()). Do not sort lists.
- Literals still come before sub-tables; sorting applies within each bucket.
- `sorted()` on mixed-type keys raises a bare TypeError before `format_key_part`'s clearer message. Validate keys first or sort on the formatted key.
- Plumb the option through `Context`; `inline_table_cache` (keyed by id) is unaffected.
- Enabling the default changes Acme's output once (a reordering relative to the previous drop). Warn their reviewers.

## Failed approaches
- None so far. Note: sort_keys validates keys via `format_key_part` before sorting so mixed-type keys give the clear 'Invalid mapping key' TypeError.
