# Private notes: local__query-string-1191489607

- 2026-11-06: While the package is on 10.x, all new behaviour must be opt-in (default off) and must not change anything for existing callers; many dependents use ^10. Reason (from user): half the org depends on ^10. Applied to parse() ignoreEmpty (default false).
- 2026-11-06: Supersedes the 2026-11-06 'all new behaviour opt-in' rule. Because 11.0.0 is being cut (breaking changes allowed), new parse()/stringify() behaviours are ON by default, with an option to switch them off. Reason (from user): opt-in flags never get turned on by anyone. Exception: parse() ignoreEmpty stays default false, because the reports service relies on it being off.
