# Private notes: local__humanize-2187290473

- 2026-11-05: humanize is used only on customer billing/usage pages; new helpers (e.g. percent) are added for that use case.
- 2026-11-05: humanize output must match billing's invoice generator exactly: percent() rounds ties half up (Decimal on repr), not Python float formatting (0.0625 -> '6.3%', not '6.2%'). Apply the same rule to any new rounding helper. Negative ties round away from zero - my choice, not confirmed with billing.
- 2026-11-05: gigabytes() in filesize.py follows the billing rule: Decimal(repr(value)) scaled by 10**9, ROUND_HALF_UP (negative ties away from zero - my choice, unconfirmed). Not naturalsize's float %-format. Reuse this for future billing helpers.
