# HANDOFF

## State
`cleanDoubleSlashes(input, respectQueryAndFragment?)` implemented in `src/utils.ts`; when true, only the part before the first `?` or `#` is cleaned. Default behaviour unchanged. Tests in `test/double-slash.test.ts`, README updated. Tests and `tsc` pass. Not committed.

## Decisions
- Split at the first `?` or `#` (whichever comes first) and recurse on the prefix, so the existing `://` handling is reused and the query/hash are appended verbatim.
- Positional boolean arg, matching the trailing-slash helpers.

## Failed approaches
None.
