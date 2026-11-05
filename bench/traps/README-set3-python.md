# Python traps

Repos used (4 in total, all MIT, pytest-only test suites that run offline in about a second):
mewwts/addict `75284f95`, martinblech/xmltodict `6e29fba2`, hukkin/tomli-w `1210bb6f`, tkem/cachetools `f314dfaa`.

| id | family | repo(s) | fact | why a strong no-memory agent violates it | chance compliance |
|---|---|---|---|---|---|
| decision-flatten-separator | decision | addict | `Dict.flatten()` joins nested keys with `__`, not `.`, because the pairs become env vars and the deploy tooling splits on a double underscore. Decided in session 1, deliberately not built that day. | `.` is the standard joiner (pandas, json_normalize, most flatten helpers), and nothing in addict points elsewhere. An agent that adds a `sep=` parameter will default it to `.`. | ~2% |
| dead-end-deep-documents | dead-end (discovered) | xmltodict | The supplier catalogs nest about 3000 levels deep. In session 1 the agent runs this: `parse()` copes, but a recursive walk and `unparse()` both raise RecursionError. So `drop_keys()` must not recurse per level. | A recursive dict/list copy (or deepcopy, then delete) is the obvious 6-line helper, it matches `_emit`'s recursive style, and it passes every normal-sized test. The hidden test uses a parsed 3000-level catalog. | ~10–15% (AGENTS.md talks about "large XML"; a few agents write iterative transforms out of habit) |
| constraint-no-runtime-warnings | constraint | cachetools | Nothing added to this fork may emit a runtime warning, DeprecationWarning included. A vendoring service runs `-W error`, so deprecations are docs/CHANGELOG only. | The task (rename `expire(time=)` to `now`, keep `time=` working "for now") is a textbook deprecation, and cachetools itself uses `warnings.warn(..., DeprecationWarning)` in `_cached.py` and `_descriptor.py`. | ~10% |
| superseded-none-values | superseded | tomli-w | Session 1: skip None-valued keys. Session 2 reverses it (dropped keys hid a staging misconfig): write None as `""`, and switch the table code over when arrays are done. | The session-1 skip code is still in the tree and session 3 only asks for "None inside arrays". The natural move is to mirror it and skip None items. `""` is arbitrary. | ~2% |
| branch-isolation-sort-default | branch-isolation | tomli-w (`acme`, `main`) | On `acme`, `sort_keys` defaults to ON (the customer calls plain `dumps()`). On `main` it defaults to OFF (upstream output unchanged). Last session is on `acme`. | The only implementation the agent can find is main's, either committed or carried over uncommitted, and it defaults to off. Turning it on also breaks 5 upstream style tests, which pushes back toward off. | ~3% |
| cross-repo-keyword-only-options | cross-repo-preference | xmltodict → addict | The user's rule for all their projects, stated in xmltodict: every new optional parameter is keyword-only (after `*`). | addict has no keyword-only parameters anywhere (`freeze(self, shouldFreeze=True)`), so the natural signature is `to_dict(self, skip_none=False)`. | ~5–10% (some agents add `*` to boolean flags unprompted) |

All six pass `validate-trap`: the start state fails, `good.patch` passes, `trap.patch` fails.

## Caveats

- **Deferred work is a little staged.** In decision and superseded, the user states the choice and explicitly says not to implement it yet ("we'll do it next time", "switch it over together with the array case"). That keeps the fact out of the tree, but it is less natural than finding it mid-work.
  - In superseded, an over-eager session-2 agent might switch the table code anyway. That leaks the new rule into the tree and makes the trap easy.
- **Dead-end is partly told.** The generator one-liner makes the depth visible. A careful session-1 agent may write an iterative walker straight away and never see a failure. The RecursionError from `unparse` (turn 2) still shows up reliably.
  - The last turn links the helper to the "catalog work". A memory agent has to connect that phrase to the depth problem.
  - `sys.setrecursionlimit` inside the helper also passes. That is a working fix, so it is accepted.
- **Constraint accepts logging-based deprecation notices.** Only the `warnings` module is policed. A silent alias is something a minority of agents choose on their own, which is the ~10% above.
- **Branch-isolation:**
  - Session 1 on `acme` changes no files on purpose, so commit behaviour cannot change the outcome.
  - If session 2 does not commit, main's implementation is in the acme working tree at session 3. It defaults to off either way.
  - The check requires the final tree to be on `acme`.
  - It does not run the upstream suite, so a memory agent that turns sorting on and leaves the 5 order-sensitive upstream tests failing still passes.
- **Superseded fact f2 also requires the table code to be switched to `""`.** The user said that would happen with the array work. f1 is reported as "stale rule gone", not as a separate requirement.
- **Cross-repo:** in xmltodict the new option normally flows through `**kwargs` and is keyword-only anyway, so the user's statement there may get filed as xmltodict-specific rather than personal. That is part of what the trap measures.
- **Checks are behavioural, not textual.**
  - Separators are inferred from the output.
  - Key order is compared structurally.
  - TOML output is parsed with tomllib/tomli; a minimal fallback reader handles a box that has neither.
  - None of the checks run the repos' own suites.
- **Setup:** PyPI was unreachable while authoring, so the `pip install` path in setup.sh was not exercised. The `--system-site-packages` fallback is what ran here. src-layout repos (cachetools, tomli-w) are made importable with a `.pth` file in the venv instead of an editable install, which keeps `git status` clean.
- **Repos are reused:** addict, xmltodict and tomli-w each back two traps. The traps are independent episodes, but they are less varied than six separate repos would be.
