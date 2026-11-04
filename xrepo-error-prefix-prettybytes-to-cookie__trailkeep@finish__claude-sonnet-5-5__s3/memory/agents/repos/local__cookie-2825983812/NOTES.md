# Private notes: local__cookie-2825983812

- 2026-11-04: stringifySetCookie throws TypeError when maxAge > 34,560,000s (400 days) because browsers silently cap cookie lifetime and callers should know. New error messages are prefixed 'cookie: ' per the user's global preference; older messages in this package (e.g. 'option maxAge is invalid') are still unprefixed, so the styles are mixed. parseSetCookie deliberately does not enforce the cap.
