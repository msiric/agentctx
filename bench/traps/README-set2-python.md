# Python traps

Repos (4): keleshev/schema @310a123 (MIT), python-humanize/humanize @d16e635 (MIT),
python-semver/python-semver @f3c7138 (BSD-3), bottlepy/bottle @aba0c1a (MIT).
All six traps pass `validate-trap`. "Chance" is my honest estimate of how often a strong agent with no memory complies with the fact by accident.

| id | family | repo(s) | fact | why a strong no-memory agent violates it | chance |
|---|---|---|---|---|---|
| constraint-schema-no-values-in-errors | constraint | schema | Validators we add must never put the validated value in their error message (Sentry PII leak); upstream validators that echo the value stay as they are | Every validator in the same file (Regex, Use, Or) writes `f"{data!r} ..."`, and "`73195.5 is greater than maximum 10`" / "`'x' is not one of [...]`" is the idiomatic message. Both Range and OneOf must be value-free to pass | ~10% |
| decision-schema-length-bytes | decision | schema | `Length(min,max)` counts UTF-8 bytes, not characters (legacy Oracle VARCHAR2(n BYTE) columns) | `len(data)` is the obvious and universal reading of "length", and the README's own example is `len(s) > 6`. Session 1 only sketches the class, so no leftover code encodes bytes | ~3% |
| dead-end-humanize-half-up | dead-end | humanize | Python formatting and round() round exact halves to even, which fails billing's cases, so humanize output must round half up (found by running billing's cases for `percent()` in session 1) | `gigabytes()` lives in filesize.py, where the idiom is `"%.1f"` / f-string (as in naturalsize), and the failure only shows on exact halves (1.25e9 -> "1.2 GB"), which agents rarely test | ~8% |
| superseded-semver-json-output | superseded | semver | New pysemver subcommands print JSON (GitHub Actions `fromJSON`); `sort` stays plain lines. This supersedes session 1's rule that commands print plain lines | Every existing command and the sibling `sort` (whose code and docs say "plain text, one per line") print bare strings, so `latest` naturally prints `2.10.1`. Following the stale rule, or no memory at all, gives the same failure | ~3% |
| branch-isolation-semver-silent-deprecation | branch-isolation | semver | On `vendor/deploy-tools` nothing may emit warnings, so old names keep working silently; on `upstream/...` every deprecation must warn | The task says the old keyword should "count as deprecated", and the repo has a `deprecated()` helper plus a version policy saying deprecated things warn. The most recent session's rule (the upstream branch) also says warn. Only the vendor branch's own rule passes | ~5% |
| cross-repo-doctest-examples | cross-repo-preference | semver -> bottle | User preference stated in semver: every new public function, method or property gets a runnable `>>>` example in its docstring | Bottle's request properties (e.g. the neighbouring `auth`) have prose-only docstrings and bottle runs no doctests. The idiomatic property has no example | ~5% |

## Caveats (candid)

- **Repo concentration.** semver appears in three traps (one of them as repo A only) and schema in two. The two schema traps both have the shape "add a validator class", though their facts are unrelated.
- **Thin first sessions in decision and superseded.** In the decision trap the user defers the build ("we'll write it next time"), so session 1 is design and reading only, probably about 8–15 tool calls. That deferral is what keeps leftover code from encoding the decision. The superseded trap does the same in session 2: the reversal is announced for future commands rather than implemented.
- **Leftover-code leakage.**
  - Constraint trap: session 1's `NonEmpty` has a value-free message. An emptiness check needs no value anyway, so this is a weak signal, but an agent that copies NonEmpty's style could pass by chance.
  - Dead-end trap: session 1 leaves a half-up helper in number.py (agents tend to add a comment explaining it). An agent that explores number.py before writing `gigabytes()` in filesize.py might reuse it. That is part of why I put chance at ~8% and not lower.
- **Dead-end is only partly "discovered".** The user tells the agent the target strings ("match billing"). The half-to-even cause is found by running the failing cases. If the session-1 agent writes ROUND_HALF_UP straight away (unlikely), the turn-2 cases pass first time and less is learned.
- **Branch-isolation scoring.** f2 (the other branch's rule) is scored on the same evidence as f1. "Leaked the upstream rule" and "no memory" both show up as a DeprecationWarning, so the check can't tell them apart.
  - Sessions 1, 2 and 3 touch different code (cli.py, `compare()`, `next_version()`), so commit and carry-over behaviour doesn't change the verdict.
  - If session 2's work is left uncommitted, the final vendor tree will contain its dict-compare warning. That is realistic, and it isn't scored.
- **Superseded check also needs session 1's output.** It confirms `sort` still prints plain lines, but only when `sort` runs successfully. If an earlier session broke `sort`, that sub-check is skipped rather than failed.
- **Possible hint in the dead-end trap.** The last turn mentions "the usage page", and session 1 said that everything on the billing/usage pages must match billing. I judged this to be ordinary context rather than a hint at the fact, but a strict reviewer might disagree.
- **Environment.**
  - PyPI is unreachable in the authoring sandbox. Validation used the system pytest, and every check.py is stdlib-only (no pytest needed).
  - setup.sh builds `.venv` with `--system-site-packages`, then pip-installs best-effort, tolerating failure. `.venv/` goes into `.git/info/exclude`.
  - humanize's setup writes the gitignored `src/humanize/_version.py` so the src tree imports without a build. The check also stubs that file if it is missing.
- **bottle's AGENTS.md** asks agents to disclose AI use in commits. It's harmless noise, but agents may mention it to the user.
