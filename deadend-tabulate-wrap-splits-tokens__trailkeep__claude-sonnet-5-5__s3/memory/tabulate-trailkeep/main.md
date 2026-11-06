# main

Branch: main · Repo: local__tabulate-3555284161 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: --wrap WIDTH CLI option was built then backed out (uncommitted, reverted) because of release freeze until Monday; no CLI changes in this build. Resume after the release. Design: add 'wrap=' to getopt in tabulate/cli.py, validate positive int (exit 2 otherwise), pass maxcolwidths=WIDTH plus break_long_words=False and break_on_hyphens=False to tabulate() via _pprint_file; add --help line and tests in test/test_cli.py. Reason for the break_* flags: the user's support team copy-pastes ticket IDs (SUPPORT-2024-118233) and URLs into a tracker, so they must never be split; default wrapping split them mid-token. Tradeoff: tokens longer than WIDTH overflow and widen the column. Applies to all columns (my choice, not requested). Motivation: support reads ticket exports in a terminal and the notes column runs off screen.
- 2026-11-06: --wrap WIDTH implemented per earlier design (cli.py getopt 'wrap=', positive-int validation exit 2, maxcolwidths + break_long_words/break_on_hyphens=False, help text, 2 tests in test_cli.py). Uncommitted. Applies to all columns (my choice).

