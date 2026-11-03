# HANDOFF

## State
Added named export `parseBytes(string) → number` (index.js, index.d.ts, index.test-d.ts, test.js, readme.md). `npm test` (xo, ava, tsd) passes.

## Behavior / decisions
- Accepts plain numbers, `B`, binary units `KiB`…`YiB` and non-`i` units; fractions allowed (`'1.5 KiB'` → 1536); units case-sensitive.
- Non-`i` units (`kB`, `KB`, `MB`…`YB`) are powers of 1024 (`1 kB` = 1024, `1 MB` = 1048576), per the storage team (users paste sizes from Windows Explorer). Implemented in `PARSE_MULTIPLIERS`. Deliberately differs from prettyBytes (powers of 1000), so `parseBytes(prettyBytes(1000))` !== 1000; documented in readme/d.ts. `K`, `Ki`, `kb`, `mB`, `KIB` still throw.
- Optional whitespace (any `\s`, incl. nbsp) between number and unit, matching prettyBytes `space`/`nonBreakingSpace` output; surrounding whitespace trimmed; optional leading `+`/`-` since prettyBytes can emit them.
- Result is not rounded (`'0.5 B'` → 0.5). Above 2^53 bytes not exact (a number).
- No exponent notation, thousands separators, or locale decimal commas.

## Gotchas
- The "documented examples" test in test.js evaluates readme/d.ts `//=>` examples with only `prettyBytes` in scope; `parseBytes` was added to that scope.
- xo rejects irregular whitespace literals in regex (use `\s`) and non-string ava assertion messages.
