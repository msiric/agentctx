# HANDOFF

## State
Added public `register_format(name, table_format)` in `tabulate/__init__.py` (exported in `__all__`), with a test in `test/test_api.py`.

## Decisions
- `tabulate_formats` is updated in place (`[:] = sorted(...)`) because `cli.py` imports the list object; rebinding would leave the CLI's `-f` check stale.
- Validates name (non-empty str) and type (`TableFormat`); re-registering a name replaces it.
- Not added to `multiline_formats`; custom formats get no multiline folding.

## Failed
- First ad-hoc check passed 9 args to TableFormat (it takes 8 fields); my mistake, not a code problem.

## Conventions
- User wants every new public function to have a short, passing `>>>` doctest example in its docstring (they review diffs on a phone). `register_format` has one; verify with `pytest --doctest-modules tabulate/__init__.py`.
