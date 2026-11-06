# HANDOFF

## State
Release is out; the `--wrap WIDTH` patch was re-applied to cli.py and test_cli.py (uncommitted in working tree). test_cli.py: 32 passed. Still to do: commit, README/CHANGELOG entry.

## Goal
Support reads ticket exports in a terminal; the notes column runs off screen. They copy-paste ticket IDs and URLs into the tracker, so those must never be split.

## Decisions (reasons)
- Long option only, no short flag: avoids clashing with existing flags.
- WIDTH must be a positive integer; otherwise exit 2 with a stderr message.
- Reuses the library's `maxcolwidths` (applies to all columns) rather than new wrapping code.
- Passes `break_long_words=False, break_on_hyphens=False`: a token longer than WIDTH overflows rather than being cut, so IDs and URLs stay intact.

## Failed approach
- First version used library defaults for breaking. It split `SUPPORT-2024-118233` and URLs mid-token (at hyphens, slashes and mid-word), which defeats copy-paste. Fixed with the two flags above.

## Open points
- Very long URLs can still exceed the terminal width; that is the cost of not splitting them.
- Per-column widths are not supported.
- Pre-existing: `-C/--colalign` is handled in the loop but missing from the getopt short options. Untouched.
- No CHANGELOG/README entry written.
- Test-writing gotchas: `assert_equal(expected, result)` order; default `--sep` is whitespace, so use `-s ','` or `-s '\t'` for multi-word notes.

## Patch
Applied to the working tree; see `git diff` (the original patch was removed from this file).
