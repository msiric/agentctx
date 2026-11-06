# Private notes: local__humanize-703928620

- 2026-11-06: User says humanize is only used on their customer billing and usage pages; percent() is the first of several billing-oriented additions, so keep new helpers suited to that use. Reason: stated by user as context for the work.
- 2026-11-06: humanize output must match billing's invoice generator exactly (usage per GB, discounts in %). percent() rounds half away from zero on the decimal repr (Decimal ROUND_HALF_UP), not float format() half-even; billing's cases are in tests/test_number.py. Check any new rounding helper against this. Reason: user stated figures render next to billing's.
