# main

Branch: main · Repo: local__tabulate-1584580276 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: --wrap WIDTH CLI option (tabulate/cli.py) was backed out by the user during release freeze (until Monday); resume after the release. Design worked out: pass maxcolwidths=WIDTH to tabulate() plus break_long_words=False and break_on_hyphens=False, because default wrapping splits ticket IDs and URLs that support copy-pastes; validate WIDTH as a positive int (exit 2); add -w/--wrap to getopt and usage text; note lines may exceed WIDTH; add a test. Use -r csv/jsonl for multi-word notes since rsv splits on whitespace.
- 2026-11-06: --wrap WIDTH (-w) re-implemented per the design above in tabulate/cli.py with test_inprocess_wrap_option; uncommitted, awaiting user review.

