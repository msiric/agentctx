# HANDOFF

## State
Added public `register_format(name, table_format)` in `tabulate/__init__.py` (exported in `__all__`), with a test in `test/test_api.py`. Full suite passes.

## Decisions
- `tabulate_formats` is mutated in place (`[:] = sorted(...)`), not rebound, because `tabulate/cli.py` imports it by name and a rebind would leave the CLI's `-f` check stale.
- Validates `name` (non-empty str) and `table_format` (TableFormat instance).
- Custom formats are not added to `multiline_formats`, so they get no multiline-cell folding.

## Failed approaches
- First test attempt built `TableFormat` with the wrong field count (it has 8 fields); fixed.

## Convention
User wants a short, passing `>>>` doctest example in the docstring of every public function added (any repo). `register_format` has one (4 examples, verified via doctest runner).
