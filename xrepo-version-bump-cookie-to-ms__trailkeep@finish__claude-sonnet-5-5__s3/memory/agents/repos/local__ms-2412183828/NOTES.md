# Private notes: local__ms-2412183828

- 2026-11-04: Microsecond units (us, µs U+00B5, μs U+03BC, microsecond(s)) parse to n/1000; capital Greek Μ lowercases to U+03BC so parse() normalizes it to µ. format() deliberately still outputs ms only (not asked for). Shipped as 4.1.0 per the bump-version-in-same-commit rule.
