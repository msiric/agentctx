# Private notes: local__query-string-2270963069

- 2026-11-06: While on 10.x, any new behaviour must be opt-in (default off) and must not change anything for existing callers, because much of the org depends on ^10. User's rule, stated when adding parse() ignoreEmpty (default false).
- 2026-11-06: From 11.0.0 on (cut the week after 2026-11-06), breaking changes are allowed. User's rule: new parse/stringify behaviours are ON by default, with an option to switch them off, because opt-in flags never get turned on by anyone. This replaces the earlier 10.x rule that new behaviour must be opt-in/default off. Exception: parse() ignoreEmpty (which also drops empty array items) stays default false, because the reports service relies on it being off.
