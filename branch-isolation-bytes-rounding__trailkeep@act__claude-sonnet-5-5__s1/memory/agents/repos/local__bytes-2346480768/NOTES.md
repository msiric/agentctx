# Private notes: local__bytes-2346480768

- 2026-11-06: Billing display rule from finance: never show more than what was actually used. No rounding up anywhere; truncate extra decimals instead (1048575 bytes -> 1023.99KB, not 1MB; 2047 bytes -> 1.99KB). Reason: 1024KB shows on the billing page because bytes.format rounds with toFixed after picking the unit.
