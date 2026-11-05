# TypeScript/JavaScript traps

Repos (all MIT, pinned): visionmedia/bytes.js `9ddc13b6c66e0cb293616fba246e05db4b6cef4d`, jshttp/range-parser `f4bf1736f28a3e574430408c18779cf7fbaf3770`, sindresorhus/pretty-ms `a0410bb189906b25000fc118ce06ba84c07971c6`, sindresorhus/parse-ms `c065907a36031d0ec5eadd99d93d5a4caf48c376`.

| id | family | repo(s) | fact | why a strong no-memory agent violates it | chance compliance |
|---|---|---|---|---|---|
| decision-range-limit-coalesce | decision | range-parser | When there are more ranges than `limit`, return one range from the lowest start to the highest end (the CDN only caches single-range responses). | The usual answers for "too many ranges" are -1 (416), -2 (ignore the header), keep the first N, or throw. Merging into one span is a product decision nothing in the code points to. | ~5% |
| dead-end-bytes-decimal-float | dead-end (discovered) | bytes | For `parse(v, {decimal: true})`, multiplying the float by 1000^n and flooring loses a byte ('2.01 kB' -> 2009). The decimal string has to be scaled exactly. Found in session 1 by running the vendor's values, then the spike is reverted. | The obvious extension is `Math.floor(1000^n * parseFloat(x))`, the same pattern parse already uses. That pattern is exact for 1024^n, so the existing tests and the usual '1.5 kB' tests pass. Math.round doesn't help either, because it fails the task's flooring requirement ('1.0007kB' -> 1000). | ~8% |
| constraint-bytes-no-regex | constraint | bytes | No new or changed regexes in the library without AppSec sign-off. New parsing has to use plain string handling. | Adding KiB/MiB/... is a one-line change to the alternation in `parseRegExp`, and every engineer makes it. | ~3% |
| superseded-range-size-no-throw | superseded | range-parser | f1 (session 1): a NaN size throws a TypeError. f2 (session 2): don't throw, return -2 (the edge worker dies on exceptions). The change was deferred. | Session 1's `throw new TypeError` for NaN, and its test, are still in the tree, next to the existing str TypeError. Extending the throw to the other bad sizes is the obvious, consistent move. | ~2% |
| branch-isolation-bytes-rounding | branch-isolation | bytes | On `billing-ui`: never show more than the actual value, cut decimals off (1048575 -> 1023.99KB). On `capacity-alerts` the opposite holds: round up (1MB). The last session is on `billing-ui`. Neither earlier session edits code. | The textbook fix for "1024KB" is to move up a unit (1MB). If memory mixes up the branches, you get round-up, and that violates billing's rule too. | ~5% (no memory); ~0% if the other branch's fact is applied |
| cross-repo-error-prefix | cross-repo-preference | pretty-ms -> parse-ms | All of the user's packages start error messages with the package name ('parse-ms: Expected ...'), because his log collector drops stack traces. | parse-ms's own messages are a plain `Expected ...`, and the new message copies that style. | ~2% |

## Caveats

- The decision, superseded and branch-isolation traps all use a "decide now, implement later" turn. Without it, the earlier session's code would give the fact away. Each one gives a reason for the delay (finance sign-off, ops review, waiting to do all the size cases together), but it is a recurring pattern, and the decision trap's session 1 is discussion only, so it's light on tool calls.
- In two traps the earlier session's agent can leak the fact:
  - dead-end: if session 1 doesn't revert the spike, or picks an exact method from the start, the last session's tree or memory has less to go on. "Floored like parse does today" pushes session 1 toward the naive approach.
  - superseded: session 2 might leave a TODO comment about the reversal in the code.

  Either leak only makes it easier for no-memory agents to pass. It can't make a valid run fail.
- branch-isolation: sessions 1 and 2 are told not to change any code, so uncommitted work can't cross `git checkout`. If an agent drafts code anyway and leaves it uncommitted, the draft follows it onto the other branch.
- constraint: f1 is a static check. A small tokenizer pulls the regex literals out of every non-test .js file and compares them with the pinned index.js; removing a regex is allowed, and any `RegExp(` call is flagged. Two risks:
  - If the session-1 agent edits a regex during the audit (it isn't asked to) and leaves the edit uncommitted, the last session fails no matter what it does.
  - Moving parsing into a new lib file that contains a regex counts as a violation. That is deliberate, since it breaks the rule in spirit.
- bytes hosts three traps and range-parser two. The traps are independent, but the domains overlap: two bytes traps add units to parse(), and two range-parser traps add new rejection paths.
- The hidden checks only load `index.js` from the working tree, with no build step, using node built-ins (plus `git show` with a fallback in the constraint trap). In this sandbox the npm registry was blocked, so `setup.sh` installs failed, as they're allowed to. The existing suites were checked at the pinned commits: mocha suites through a small describe/it shim, pretty-ms/parse-ms with `node --test`. All pass.
- The dead-end fact is a float subtlety. A very careful agent might see it coming without memory, so the ~8% estimate is the least certain one here.
