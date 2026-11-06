# HANDOFF

## State
Branch `acme-feed`: Acme's nightly job runs `tabulate -r jsonl -f tsv`; their dumps end with blank lines, which crashed the jsonl reader.

Done: `_read_jsonl_file` in `tabulate/cli.py` now skips blank/whitespace-only lines. Added `test_inprocess_jsonl_skips_blank_lines` in `test/test_cli.py`.

## Decisions
- Filter with `row.strip()` so whitespace-only lines are skipped too, not only empty ones.
- Malformed non-blank lines still raise (not silently swallowed).

## Failed approaches
None.

## Missing values (Acme) - done
Records lacking a key now render `.` (SAS loader marker) instead of an empty cell. `_main` sets `missingval = _JSONL_MISSINGVAL` (`"."`) for `-r jsonl` only and passes it through `_pprint_file` to `tabulate(...)`. rsv/csv are unchanged (still empty). Test: `test_inprocess_jsonl_missing_key_uses_marker`.

Decisions:
- Fixed default for jsonl, no flag: the cron command `tabulate -r jsonl -f tsv` can't take extra flags.
- CONFLICT to resolve: Globex (below) wants `NA` for the same `-r jsonl` path. A fixed `.` default breaks them; merging both branches needs a flag/option (e.g. `--missingval`) with `.` as the jsonl default, or per-feed config. Not decided.

## Globex feed (branch `globex-feed`)
Globex also runs `tabulate -r jsonl -f tsv` and wanted column selection.

Done: `--columns a,b,c` (long option only) in `tabulate/cli.py`. For jsonl, each record is projected to those keys in that order; a key missing from a record becomes an empty cell (None). Test: `test_inprocess_jsonl_columns`.

Decisions:
- jsonl only; using `--columns` with rsv/csv exits with status 2 and an error, since those have no keys.
- Projection happens in `_read_jsonl_file`, before tabulate, so `--headers keys` follows the chosen order; with `--headers KEY:HEADER` remapping, tabulate's own header handling applies.
- Note: tsv output from tabulate pads cells with spaces around the tabs (existing behaviour, not changed here); the new test expects that.

## Next for Globex (not started, waiting on sign-off)
Globex loads the feed with R, so missing values must render as `NA`. User will do this once Globex has signed off on the column list. Likely hook: `missingval="NA"` in the `tabulate(...)` call in `_pprint_file`, but it's untested and not decided whether it should be a flag or fixed for this feed.
