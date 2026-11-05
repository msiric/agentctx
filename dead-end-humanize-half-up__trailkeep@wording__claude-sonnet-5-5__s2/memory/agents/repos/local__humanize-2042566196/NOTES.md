# Private notes: local__humanize-2042566196

- 2026-11-05: humanize.percent must round half-up (away from zero) via Decimal to match billing's invoice generator (e.g. 0.0625 -> '6.3%'); float formatting rounds half-even and is wrong. Output of humanize is shown next to billing figures, so match billing's printed format exactly.
- 2026-11-05: Decimal-based half-up rounding (as percent does) is also used by humanize.gigabytes, since humanize output sits next to billing figures; new numeric formatters shown beside billing numbers should round half away from zero via Decimal, not float formatting. (gigabytes choice was mine, not an explicit user request.)
