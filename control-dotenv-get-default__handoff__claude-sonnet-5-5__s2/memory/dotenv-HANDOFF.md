# Handoff

## State
`dotenv get KEY --default VALUE` implemented in `src/dotenv/cli.py`; 6 tests added in `tests/test_cli.py`. All pass.

## Decisions
- Default is used only when the key is missing or bare (value None). `KEY=` (empty string) still prints empty, not the default.
- `--default ""` is honored (checked `is not None`, not truthiness).
- An unreadable/missing env *file* still exits 2: the default covers missing keys, not I/O errors.

## Notes / gotchas
- A different `dotenv` is installed in site-packages and shadows `src/`. Run tests with `PYTHONPATH=src`, otherwise the new option shows as "no such option".
- 5 pre-existing failures in tests/test_cli.py (`test_file_option_expands_user[*]` etc.) fail identically without my change; not investigated.
