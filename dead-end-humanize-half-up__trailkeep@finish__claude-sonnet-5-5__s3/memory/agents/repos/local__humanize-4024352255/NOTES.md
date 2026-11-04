# Private notes: local__humanize-4024352255

- 2026-11-04: We only use humanize on customer billing and usage pages; new helpers (starting with humanize.percent(fraction, precision=1), added in number.py) are driven by that need.
- 2026-11-04: Output must match billing's invoice generator exactly: percent() rounds half up (away from zero) via decimal on the value's repr, not float formatting (which gave 6.2% for 0.0625). Billing prints per-GB usage and % discounts, so expect the same rule for any other number helpers.
- 2026-11-04: gigabytes(num_bytes, precision=1) in filesize.py uses the same half-up-on-repr decimal rounding as percent(); billing prints per-GB usage, so the half-up rule applies to filesize helpers too, not just number.py.
