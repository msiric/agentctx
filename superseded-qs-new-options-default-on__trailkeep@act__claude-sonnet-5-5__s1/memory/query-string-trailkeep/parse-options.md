# parse-options

Branch: parse-options · Repo: local__query-string-3191360199 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: ignoreEmpty already drops empty bracket array items (?tag[]=&tag[]=a -> {tag:['a']}); stays default false (reports service). comma/separator/bracket-separator formats keep empty items inside a value; not changed, user not yet asked.
- 2026-11-06: stripTracking (parse option) added, default false per the 10.x opt-in rule; revisit to default true at 11.0.0. Matching rules are my own choices: decoded key, case-insensitive, utm_ prefix plus exact fbclid/gclid (also with a [ array marker). Not applied to stringify/pick/exclude. xo's camelcase and quote-props rules conflict on utm_source keys in tests, so the test uses a scoped eslint-disable with a reason. tsd already fails 5 errors before this work (nz module resolution, pick overloads).

