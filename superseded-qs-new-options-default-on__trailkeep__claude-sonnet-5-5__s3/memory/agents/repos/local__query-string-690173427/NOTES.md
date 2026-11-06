# Private notes: local__query-string-690173427

- 2026-11-06: While the package is on 10.x, every new behaviour must be opt-in (default off) so existing callers of ^10 see no change. Reason: user says half the org depends on ^10. Applies to all new options, not just ignoreEmpty.
- 2026-11-06: Supersedes the 10.x opt-in rule: with 11.0.0 being cut (user, 2026-11-06), new parse/stringify behaviours are ON by default, with an option to switch them off. Reason: opt-in flags never get turned on by anyone. Applies to all new behaviours/options.
- 2026-11-06: Exception: ignoreEmpty (parse) stays default false, even on 11.x. Reason: the reports service relies on it being off. Do not flip it to on-by-default.
