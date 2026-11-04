# HANDOFF
- Added opt-in `respectQueryAndFragment` 2nd arg to `cleanDoubleSlashes` (src/utils.ts): splits input at first `?`/`#`, cleans only the prefix. Default unchanged.
- Tests in test/double-slash.test.ts; README updated.
- Decision: split on first `?` or `#` (whichever first) since both begin non-path data.
