# HANDOFF

## State
Branch `storage-app`: named export `parseBytes(string): number` (index.js, index.d.ts, tests in test.js, type test in index.test-d.ts, readme section). `npm test` passes (xo, ava, tsd).

Supported: plain numbers, `B`, binary units `KiB`..`YiB`, and non-`i` units `kB`, `KB`, `MB`..`YB`. Fractions (`'1.5 KiB'` -> 1536), optional leading `+`/`-`, optional single space (or NBSP) before the unit, surrounding whitespace trimmed. Units are case-sensitive; bare `K`, `k`, `Kb`, `mB`, `gb`, `bit` throw.

## Decisions
- Non-`i` units are powers of 1024 (`1 KB` = `1 kB` = 1024, `1 MB` = 1048576), per the storage team: users paste sizes from Windows Explorer. This deviates from prettyBytes' own output where `kB` is 1000, so the round-trip test only covers binary output. Documented prominently in readme and index.d.ts.
- Bad input throws: `TypeError` for non-strings, `SyntaxError` for unparsable strings/units.
- Result is not rounded. Scaling by 1024**n is exact.
- Exponents, `Infinity`, thousands separators rejected.
- Readme section is prose-only (no ```js fence): test.js extracts every ```js `//=>` example from readme/d.ts and evaluates it as a prettyBytes call, so parseBytes examples there would break it. Adapting that test would allow examples.

## Failed approaches
- Literal NBSP in the regex trips xo `no-irregular-whitespace`; use ` `.
