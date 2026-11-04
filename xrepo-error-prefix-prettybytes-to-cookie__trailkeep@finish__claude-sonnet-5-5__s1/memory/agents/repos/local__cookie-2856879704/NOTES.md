# Private notes: local__cookie-2856879704

- 2026-11-04: stringifySetCookie throws TypeError when maxAge > 400 days (34,560,000s) because browsers cap cookie lifetimes at 400 days and silently shorten longer ones; limit is inclusive.
