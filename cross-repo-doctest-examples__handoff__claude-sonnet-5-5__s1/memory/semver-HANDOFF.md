# HANDOFF

- Task: add `Version.is_prerelease` (src/semver/version.py), tests in tests/test_is_prerelease.py, changelog fragment changelog.d/is_prerelease.feature.rst.
- Decision: implemented as `bool(self._prerelease)` so an empty-string prerelease (allowed by the constructor) counts as absent, matching `__str__`.
- Read-only property, no setter beyond default AttributeError (property without setter).
- Failed approaches: none.
- Docstring of `is_prerelease` has a `>>>` doctest (verified with --doctest-modules). User wants this for every new public function/method/property in all projects.
