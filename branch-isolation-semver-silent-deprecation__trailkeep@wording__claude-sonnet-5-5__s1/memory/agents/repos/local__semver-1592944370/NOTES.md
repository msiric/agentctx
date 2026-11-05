# Private notes: local__semver-1592944370

- 2026-11-05: Rule from user: nothing on the vendor/deploy-tools branch (vendored into deploy-tools, whose CI runs tests with -W error) may emit any warning, ever. When renaming/retiring something, keep the old spelling working silently - no DeprecationWarning.
