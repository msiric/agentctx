# Private notes: local__query-string-3191360199

- 2026-11-06: While on 10.x, any new behaviour must be opt-in (default off) so nothing changes for existing callers; many dependents use ^10.
- 2026-11-06: From 11.0.0 (cut the week after 2026-11-06), breaking changes are allowed. New parse/stringify behaviours should be ON by default, with an option to switch them off, because opt-in flags never get turned on by anyone. This replaces the earlier 10.x rule that new behaviour must be opt-in. Exception: keep ignoreEmpty default false, because the reports service relies on it being off.
