# HANDOFF

Task: Acme nightly feed pipes dumps through `tabulate -r jsonl -f tsv`; dumps end with blank lines which crashed the jsonl reader.

Done: `_read_jsonl_file` in tabulate/cli.py skips whitespace-only lines (`if row.strip()`). Test added in test/test_cli.py.
Decision: skip only blank lines; malformed non-blank lines still raise, so bad data isn't silently hidden.
Failed approaches: none.

Done (uncommitted): missing jsonl keys now give `.` (Acme's SAS loader marker). The cron command has no flags, so for `-r jsonl` the default missingval is `.`; new `-m/--missingval STR` overrides it (non-jsonl default stays empty). Tests added in test/test_cli.py.
Decision: default lives in cli.py keyed on jsonl, not in the library's `_DEFAULT_MISSINGVAL`, so the library API is unchanged.
Failed approaches: none.

## Globex feed (branch globex-feed)
Done: `--columns a,b,c` (jsonl only) keeps only those keys in that order; missing keys give empty cells. Implemented in `_read_jsonl_file(columns=...)`; test added.
Decision: non-jsonl input with --columns exits 3 with an error rather than silently ignoring it.
Failed approaches: none.

Next (not started, waiting on Globex sign-off of the column list): Globex loads the feed with R, so missing values must come out as `NA` (cf. Acme's `.` above; `-m NA` from the Acme change now provides the override, though the jsonl default is `.`, so Globex must pass it or the default needs a per-feed rework). Owner: user will do it.

Note: HANDOFF.md had stash-pop conflict markers (Globex notes from stash@{0}); resolved by keeping both sections. The stash is still in `git stash list`.
