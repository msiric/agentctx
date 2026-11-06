# Private notes: local__semver-1838642911

- 2026-11-06: On the vendor/deploy-tools branch (semver vendored in deploy-tools), nothing may emit any warning (DeprecationWarning etc.), because their CI runs with -W error; when renaming/retiring something, keep the old spelling working silently.
