# main

Branch: main · Repo: local__pretty-bytes-823692542 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: unit option (1cb5030): validated at runtime against the bits/binary unit set, TypeError otherwise; forced unit skips the auto exponent and rounding-bump corrections. TS type is a plain union, not tied to bits/binary. Not pushed.
- 2026-11-04: significantDigits option: integer 1-100, invalid values silently ignored (default 3) per repo rule that new options never throw; ignored when fraction-digit options are set. Not committed.

