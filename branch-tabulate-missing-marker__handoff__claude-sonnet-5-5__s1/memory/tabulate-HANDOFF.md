# HANDOFF

## Task
Acme nightly feed runs `tabulate -r jsonl -f tsv`.
1. Their dumps end with blank lines, which crashed the jsonl reader. (done, d8e7706)
2. Records missing a key must get the loader's missing-value marker instead of an empty cell. (done, uncommitted)

## State
- `_read_jsonl_file` in `tabulate/cli.py` skips blank/whitespace-only lines. Test: `test_inprocess_jsonl_skips_blank_lines`.
- New `--missingval STR` option in `tabulate/cli.py`, passed through to `tabulate(missingval=...)`. For `-r jsonl` the default is `.` (Acme loads with SAS, missing = `.`); other input formats keep `""`. Tests: `test_inprocess_jsonl_missing_values_default_to_dot`, `test_inprocess_jsonl_missingval_option`. All 32 CLI tests pass.

## Decisions
- `if row.strip()` filter for blank lines, matching `_read_rsv_file`. Blank lines are skipped anywhere.
- Default `.` is set per input format (jsonl only) rather than globally, because the cron command has no extra flags and must work as is; csv/rsv output is unchanged.
- Made it an option, not a hardcode, because Globex (R loader) needs `NA`; they can pass `--missingval NA`.
- Explicit JSON `null` values also render as the marker (tabulate treats None as missing).

## Failed approaches
None.

## Housekeeping
HANDOFF.md was in a merge-conflict state (`UU`) from a stash pop of `stash@{0}` (made on branch `globex-feed`). I resolved it keeping the Acme notes. The Globex notes (`--columns` option, `NA` requirement) are still in `stash@{0}`; the stash was not dropped. Note the `--columns` code itself is not on this branch.
