# billing-ui

Branch: billing-ui · Repo: local__bytes-866991639 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: bytes.format shows '1024KB' near unit boundaries because toFixed rounds up after the unit is chosen (index.js lines 112-113). Fix direction agreed with the user: truncate (floor) to decimalPlaces instead of rounding, so no unit bump. NO code changes yet: finance still has to sign off the wording on the billing page. Don't edit until the user says finance approved.
- 2026-11-06: bytes.format now truncates (Math.trunc on scaled value) instead of toFixed rounding; finance approved on 2026-11-06. Existing tests that expected round-up (1.5kb dp0 -> 2kb, 1.05kb dp1 -> 1.1kb) were changed to truncated values. Other billing-displayed numbers must also truncate.

