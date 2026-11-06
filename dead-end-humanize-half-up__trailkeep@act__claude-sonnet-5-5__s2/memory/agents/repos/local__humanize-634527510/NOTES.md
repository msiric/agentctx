# Private notes: local__humanize-634527510

- 2026-11-06: User context: their team uses humanize only on customer billing and usage pages, so new helpers should target those (e.g. percent, added first as humanize.percent(fraction, precision=1)). Choice of mine: percent follows scientific()'s handling of non-numeric/non-finite input (returns str(value) / NaN / +Inf / -Inf) rather than raising.
- 2026-11-06: humanize output must match billing's invoice generator exactly (usage per GB, discounts in %). percent() rounds half up on the decimal repr (0.0625 -> '6.3%'), NOT Python's float formatting (gives '6.2'). Keep that when adding/changing helpers; check billing's rounding for others (e.g. GB sizes).
- 2026-11-06: gigabytes(num_bytes, precision=1) is in filesize.py: rounds half up on decimal repr (1.25e9 -> '1.3 GB') to match billing, and (my choice) handles non-numeric/non-finite input like percent() (str(value)/NaN/+Inf/-Inf). Keep new billing helpers consistent with this.
