# Private notes: local__ms-1700307145

- 2026-11-06: Microsecond units (us, µs, microsecond(s)) parse to n/1000. The regex also accepts Greek μ (U+03BC) because /i matches it and toLowerCase() turns an uppercased µ into μ. parse() normalizes it back to µ. Strict StringValue types deliberately exclude μ (my choice). Version was bumped 4.0.0 -> 4.1.0 in the same change, per user's rule.
