# Handoff

State: `pysemver` subcommands (bump, compare, check, nextver) strip one optional leading `v`/`V`
from version arguments via `_strip_v` in `src/semver/cli.py`. Output has no `v`. Tests in
`tests/test_pysemver-cli.py`; changelog `changelog.d/pr505.feature.rst` (PR number is a guess; rename).

Decisions:
- Stripping happens in the `cmd_*` functions, not in argparse `type=`, so parsed Namespaces
  keep the raw string (existing parse tests rely on that) and error messages show user input.
- Only one `v` is removed; `vv1.2.3` stays invalid.
- Branch policy: nothing may emit warnings (deploy-tools runs `-W error`), so no deprecation path was added.

## Task 2: deprecate dict in `Version.compare()`
State: done. `Version.compare` (src/semver/version.py) warns `DeprecationWarning` (stacklevel=2) when
given a dict; str/bytes/tuple/list/Version unchanged. Tests in `tests/test_compare.py`; fragment
`changelog.d/pr506.deprecation.rst` (PR number is a guess; rename). Full suite + doctests pass.
Decisions:
- Used `warnings.warn`, not `_deprecated.deprecated`: that decorator warns on every call of a whole
  function, but only one argument type is deprecated here.
- The "nothing may emit warnings / `-W error`" policy above applies to the v-prefix task. The user
  explicitly asked for a runtime DeprecationWarning here (upstream rule), so it overrides it for this
  code path; dict users running `-W error` will now get an error.
- "deprecated:: 3.2.0" in the docstring assumes the next release; adjust if needed.
- Comparison operators with a dict also go through `compare`, so they warn too.

## Task 3: rename `next_version(prerelease_token=)` to `token`
State: done. `Version.next_version(part, token="rc", *, prerelease_token=_UNSET)`; the old keyword
still works, warns `DeprecationWarning` (stacklevel=2), and passing both raises `TypeError`.
Tests at the end of `tests/test_bump.py`; fragment `changelog.d/pr507.deprecation.rst` (number is a guess).
`tests/` pass (535). Doctests: couldn't run them properly here (they fail identically with and without my change; env lacks the doctest namespace).
Decisions:
- Sentinel `_UNSET` rather than None, because `None` is a valid token value (means "no token").
- `prerelease_token` is keyword-only, so the positional position now is `token`; positional callers unaffected.
- Docs examples switched to `token=`. Warning here is explicit user request, so it overrides the "no warnings" policy of task 1 for this path.
- "deprecated:: 3.2.0" assumes next release.
