# Private notes: local__bytes-692788582

- 2026-11-05: Billing display rule from finance: never show more than was actually used. bytes.format must truncate extra decimals (toward zero), never round up: 1048575 bytes -> 1023.99KB (not 1024KB or 1MB), 2047 bytes -> 1.99KB. Cause of the '1024KB' bug is toFixed() rounding up at unit boundaries (index.js format). Status: no code changed yet; waiting on finance sign-off of the page wording.
- 2026-11-05: bytes.format: explicit options.unit is echoed back in caller's case (unit:'b' -> '0b'), not normalized.
