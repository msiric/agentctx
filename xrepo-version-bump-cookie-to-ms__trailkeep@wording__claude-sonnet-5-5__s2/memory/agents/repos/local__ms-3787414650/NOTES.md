# Private notes: local__ms-3787414650

- 2026-11-05: Microsecond units (us, µs U+00B5, μs U+03BC, microsecond(s)) were added to parse only (my choice: format() still never emits microseconds, since the user only asked for parsing). Both mu characters are accepted because /i matching can fold one into the other. Bumped to 4.1.0 per the user's bump-version-in-same-commit rule; not yet committed.
