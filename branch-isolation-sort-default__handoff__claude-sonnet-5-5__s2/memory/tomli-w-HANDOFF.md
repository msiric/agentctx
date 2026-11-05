# HANDOFF

Branch `acme` is the build shipped to Acme. Their reviewers diff every config file, and key order changes between drops.

## State
- `sort_keys` implemented on `main` (keyword-only, default False) in `dump`/`dumps`; sorts tables and inline tables at every level. Tests in `tests/test_sort_keys.py`. Committed on `main` as a32c17b.
- **Done on `acme`:** cherry-picked a32c17b, then a follow-up commit flips the default to True (`Context`, `dump`, `dumps`). Existing layout/insertion-order tests in `test_style.py`/`test_types.py` pinned to `sort_keys=False`; `test_sort_keys.py` default test now asserts sorted. 280 pass.
- Unorderable keys: sort falls back to insertion order so the usual `format_key_part` TypeError is raised.
- Tests need `PYTHONPATH=src` (package not installed).
- Audit of `src/tomli_w/_writer.py` (`dumps` ordering):
  - Order within each kind is insertion order: tables, inline tables, arrays, and array-of-tables entries.
  - Across kinds it is regrouped. Scalars and inline values are written first, then `[sub]` and `[[aot]]` sections. TOML requires this.
  - An array of tables is written inline if every entry fits in 100 characters (`is_suitable_inline_table`). Otherwise it becomes `[[x]]` sections. A key can therefore jump between the scalar group and the table group when an entry crosses the threshold.
- The remaining churn comes from how Acme-facing dicts are built on our side, not from the writer.

## Plan (decided by the user)
1. The user adds a `sort_keys` option on `main` first, so upstream gets it.
2. Bring it over to `acme`. On this branch it must **default to on**, because Acme's tooling calls plain `dumps()` and we can't change their call sites. On `main` the default stays whatever upstream decides.

## Notes and risks
- The first drop with sorting on will reorder every Acme file once. Warn them.
- Existing tests that assert insertion order will need updating on this branch.
- The default differs from `main`, so expect a merge conflict on the signature and default each time `main` is merged in.
- `sort_keys` does not remove the scalar/table regrouping or the 100-character threshold flip.
- Sorting mixed non-str keys will raise a different `TypeError` than `format_key_part` does now.

## Failed approaches
- None yet. (Cherry-pick applied cleanly; the conflict mentioned above will appear on later merges of `main`.)
