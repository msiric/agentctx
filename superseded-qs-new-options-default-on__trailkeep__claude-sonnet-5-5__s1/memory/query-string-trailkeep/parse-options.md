# parse-options

Branch: parse-options · Repo: local__query-string-1191489607 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: ignoreEmpty (default false, deliberately kept off) already drops empty bracket array items. Open question: whether to also drop empty items inside comma/separator/bracket-separator values; if added, the new-default rule applies to that part only if the user says so, since it would sit under ignoreEmpty.
- 2026-11-06: stripTracking (parse): default true per the 11.0.0 new-defaults-on rule; matches decoded key /^(utm_|fbclid$|gclid$)/, case-sensitive, so 'fbclid[]' array forms are not stripped (my choice). Opt out with stripTracking:false.

