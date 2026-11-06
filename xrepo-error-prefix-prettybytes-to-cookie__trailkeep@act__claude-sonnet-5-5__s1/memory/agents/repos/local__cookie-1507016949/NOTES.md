# Private notes: local__cookie-1507016949

- 2026-11-06: stringifySetCookie throws TypeError when maxAge > 34,560,000s (400 days, browser cap); user asked for it so callers learn of silent shortening. New error uses 'cookie: ' prefix per the user's all-repo preference; existing errors left unprefixed (my choice, to avoid changing messages callers may match on). Ask the user before prefixing them.
