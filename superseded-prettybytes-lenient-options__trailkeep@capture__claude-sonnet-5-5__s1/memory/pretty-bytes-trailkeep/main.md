# main

Branch: main · Repo: local__pretty-bytes-350161432 · Kind: branch · Created: 2026-11-03

## Decisions and dead ends

- 2026-11-03: Policy: new options must never throw on bad values - ignore and format as if option not passed. Existing 'unit' option keeps its throw until next major (user decision, after stale saved pref unit:'KB' crashed dashboard).

