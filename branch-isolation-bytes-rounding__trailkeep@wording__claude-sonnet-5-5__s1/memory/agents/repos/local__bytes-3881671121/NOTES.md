# Private notes: local__bytes-3881671121

- 2026-11-05: Billing display rule from finance (user-stated): never display more than was actually used. Anywhere billing sizes are formatted, truncate extra decimals instead of rounding (1048575 bytes -> 1023.99KB, not 1MB; 2047 bytes -> 1.99KB). Reason: finance requires displayed usage never to exceed actual usage. The '1024KB' bug in bytes.format comes from toFixed rounding up after unit selection; the fix must truncate, not round-then-step-up.
