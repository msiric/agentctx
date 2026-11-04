# HANDOFF
- Task: add `Version.is_prerelease` (src/semver/version.py), tests in tests/test_is_prerelease.py, changelog.d/pr505.feature.rst (PR number is a guess; rename to the real one).
- Decision: `bool(self._prerelease)` so empty-string prerelease is False, matching `__str__` which omits it.
- Status: implemented; full suite passes. Docstring has runnable >>> examples (verified with --doctest-modules).
- Standing user rule (added to global CLAUDE.md): every new public function/method/property needs a runnable >>> example.
