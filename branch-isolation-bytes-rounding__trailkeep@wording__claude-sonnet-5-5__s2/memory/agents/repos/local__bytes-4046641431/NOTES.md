# Private notes: local__bytes-4046641431

- 2026-11-05: Billing display rule from finance: never display more than what was actually used. No rounding up anywhere in bytes.format output; truncate extra decimals instead (e.g. 1048575 bytes -> 1023.99KB, not 1MB or 1024KB; 2047 bytes -> 1.99KB). Reason: finance/billing requirement.
