# HANDOFF
## State
`dotenv get KEY --default VALUE` implemented in src/dotenv/cli.py; tests added in tests/test_cli.py. Done.
## Decisions
- Default applies only when key is missing or bare (no `=`); empty string values still print empty.
- `--default ""` is honoured (compared with `is None`, not truthiness).
- Unreadable/missing --file still exits 2; default doesn't mask file errors.
## Failed approaches
None.
