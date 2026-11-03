# HANDOFF

## State
Added opt-in `respectQueryAndFragment` (2nd arg) to `cleanDoubleSlashes` in `src/utils.ts`. Default behaviour unchanged. Tests in `test/double-slash.test.ts`, README updated.

## Decisions
- Split at first `?` or `#`, clean only the prefix with the existing logic (so `://` protocol handling is kept), append the rest verbatim. Positional boolean matches the trailing-slash helpers.

## Failed approaches
None.
