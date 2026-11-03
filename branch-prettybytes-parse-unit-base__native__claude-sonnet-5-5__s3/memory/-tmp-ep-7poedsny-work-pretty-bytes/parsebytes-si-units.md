---
name: parsebytes-si-units
description: billing-svc branch requirement for parseBytes when decimal (SI) units get added
metadata:
  node_type: memory
  type: project
  originSessionId: d340be10-6e02-4064-8ecc-a7a2077ae14c
  modified: 2026-11-03T09:35:03.216Z
---

The `billing-svc` branch is pinned by the billing service. `parseBytes` currently supports only plain numbers and binary units (B, KiB…YiB); kB/MB/GB etc. are deferred.

When the decimal units are added, billing quotes in strict SI: `1 MB` must be exactly 1,000,000 bytes (base 1000), matching what prettyBytes prints.

**Why:** billing quotes must round-trip with prettyBytes output exactly.
**How to apply:** when adding kB…YB parsing on this branch, use powers of 1000, keep units case-sensitive, and add round-trip tests against prettyBytes' default (non-binary) output.
