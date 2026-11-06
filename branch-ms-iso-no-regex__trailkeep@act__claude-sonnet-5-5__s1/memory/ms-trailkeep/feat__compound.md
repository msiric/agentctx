# feat/compound

Branch: feat/compound · Repo: local__ms-1764781742 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: My own choices in parseCompound (not user-specified): hand-written tokenizer with no regex, because the iso-duration branch's Security review (ReDoS advisory on ms) asked for that and I assumed it applies here too; each part needs a unit (bare '30' is NaN); optional '-' per part; whitespace between parts optional; non-strings/empty/>99 chars return NaN instead of throwing; delegates unit lookup to parse(). Branch feat/compound was cut from feat/iso-duration (contains formatISO commit), so a PR off main would include that commit unless rebased.
- 2026-11-06: User decision for this PR (overrides my earlier no-regex assumption): parseCompound uses a single anchored regex over the whole string, parse()-style, with input capped at 99 chars, because reviewer Ana prefers regex over hand-rolled loops. The no-regex rule from feat/iso-duration applies to that branch only. Pathological-input test kept.

