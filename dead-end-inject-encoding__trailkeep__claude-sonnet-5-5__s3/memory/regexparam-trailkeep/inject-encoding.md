# inject-encoding

Branch: inject-encoding · Repo: local__regexparam-376074686 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: Encoding for inject() on hold: user is deciding whether it belongs in regexparam or in their uploader client. encodeURIComponent alone doesn't match the storage service (it leaves ! ' ( ) * unescaped; the service signs them as %21 %27 %28 %29 %2A). Wildcard values need per-segment encoding. Also: inject() 0 fix and tests are done but uncommitted; npm test fails on this Node (esm loader), tests were run via a temp .mjs copy.
- 2026-11-04: Encoding hold resolved 2026-11-04: user chose to put percent-encoding in regexparam inject(). Implemented (enc() also escapes ! ' ( ) *; wildcard encoded per segment, slashes kept) with tests; 38/38 pass via temp .mjs copy. All changes (incl. 0 fix) still uncommitted.

