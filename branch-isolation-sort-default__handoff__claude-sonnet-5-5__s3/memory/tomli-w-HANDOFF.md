# HANDOFF

## Task
Acme reviewers diff every config file we ship from branch `acme` and see key order jump between drops. `sort_keys` (default False) is now implemented on `main` (committed as e508697): `Context`, `dump`, `dumps`, `iter_items` helper in `_writer.py`, tests in `tests/test_sort_keys.py`, README section. Step 2 done on `acme`: cherry-picked e508697 (c8a169b) plus a follow-up commit flipping `sort_keys` default to True in `dump`/`dumps` (`Context` default stays False). Existing order-dependent tests in test_style.py/test_types.py now pass `sort_keys=False`; `test_default_sorts_keys` and the README were updated. Full suite passes with `PYTHONPATH=src`. Still to do: warn Acme reviewers that the first sorted drop diffs heavily against the last unsorted one.

## Findings (src/tomli_w/_writer.py)
- `dumps` never sorts. Keys within a table, inline-table keys and AoT element order all follow insertion order.
- Not purely insertion order: `gen_table_chunks` (L73-97) writes all scalar/array keys first, then sub-tables and arrays of tables. This is required by TOML and must stay.
- An array of dicts is written inline if each element fits in 100 chars (`is_suitable_inline_table`), otherwise as `[[aot]]` blocks. Small data changes can flip a key between the scalar and table sections.
- Root cause of the churn: our side builds dicts in varying order. The library output is deterministic for identical input.

## Decision / plan (from user)
1. User gets a `sort_keys` option added on `main` first (upstream), default False.
2. Bring it to this branch with default **True**, because Acme's tooling calls plain `dumps()` and we can't change their call sites.

## Implementation notes for when this starts
- Add `sort_keys` to `Context`, `dump`, `dumps`.
- Sort once per table in `gen_table_chunks` before the literals/tables split, and in `format_inline_table` (`obj.items()`).
- Do NOT sort array elements, including AoT; only keys inside each element.
- Non-str keys: keep the existing `format_key_part` TypeError message (sort with a key function or check types first).
- Branch difference should be just `sort_keys: bool = True` in the two signatures.
- Existing tests asserting insertion order should pass `sort_keys=False` explicitly.
- Warn Acme reviewers that the first sorted drop will diff heavily against the last unsorted one.

## Failed approaches
None. Note: tests need `PYTHONPATH=src` since the package isn't installed here.
