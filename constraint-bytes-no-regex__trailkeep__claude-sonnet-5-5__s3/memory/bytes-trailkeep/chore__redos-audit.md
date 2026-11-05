# chore/redos-audit

Branch: chore/redos-audit · Repo: local__bytes-344727597 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: ReDoS audit of index.js: parseRegExp is linear (160k-char hostile inputs <1.1ms). formatThousandsRegExp and formatDecimalsRegExp are quadratic when run directly on long input, but format() only feeds them toFixed() output (<=~21 integer digits, one dot), so they are unreachable via the public API. No code change made. Bench script was /tmp/redos/bench.js.

