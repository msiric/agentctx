# HANDOFF

## State
Added public `register_format(name, table_format)` in `tabulate/__init__.py` (exported in `__all__`),
with tests in `test/test_register_format.py`.

## Decisions
- `tabulate_formats` is updated **in place** (`[:] = sorted(...)`) because `cli.py` imports the list
  object by name; rebinding would leave the CLI's `-f` check stale.
- Re-registering an existing name (even built-in) replaces it; validates name is non-empty str and value is a `TableFormat`.
- Custom formats are not added to `multiline_formats` (default multiline handling applies).

## Failed approaches
None.

## Update: docstring example
- `register_format` docstring has a `>>>` doctest (cleans up after itself). Passes via `pytest --doctest-modules` and
  `doctest.run_docstring_examples` on the imported module.
- Fails under `python -m doctest tabulate/__init__.py` (runs file as a script, so `TableFormat` is a different class
  and the isinstance check rejects it). Not an issue with the code; use the import-based runners.
- User preference: every public function I add gets a short passing `>>>` example.
- Nothing committed yet.
