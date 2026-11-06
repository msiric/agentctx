# feature/billing-numbers

Branch: feature/billing-numbers · Repo: local__humanize-703928620 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: Added humanize.percent(value, precision=1) in number.py, exported in __init__, tests in tests/test_number.py. My choice (not the user's): non-numeric input returns str(value) and nan/inf use _format_not_finite, mirroring scientific().
- 2026-11-06: Added humanize.gigabytes(num_bytes, precision=1) in filesize.py (exported, tests in tests/test_filesize.py). Rounds half away from zero on the decimal repr (Decimal ROUND_HALF_UP) to match billing, same as percent(). My choice: non-numeric input returns str(value), inf/nan return str(value); ints use exact Decimal.

