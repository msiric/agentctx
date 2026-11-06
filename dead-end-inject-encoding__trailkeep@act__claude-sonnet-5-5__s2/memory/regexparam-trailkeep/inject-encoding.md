# inject-encoding

Branch: inject-encoding · Repo: local__regexparam-136079622 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: Encoding for inject() is on hold: user is deciding whether it belongs in regexparam or in their uploader client. Don't add it until they decide. Finding: plain encodeURIComponent does NOT match the storage service's signed path, because it leaves ! ' ( ) * raw. Encoding those five as uppercase %XX after encodeURIComponent matched the one logged example (Tom's Q3 report (final)!.pdf). Other characters (unicode, ~, +, &) are unverified.
- 2026-11-06: Fixed inject() dropping numeric 0 (check is now x || x === 0). '' / null / undefined / false are still treated as missing, which was my choice to keep the change narrow. Added tests in test/inject.js. Changes are uncommitted.
- 2026-11-06: inject() now percent-encodes values (user asked to resume, lifting the earlier hold). My choices: encodeURIComponent plus ! ' ( ) * as uppercase %XX (matches the storage service's logged example); wildcard '*' values are split on '/' and each segment encoded so slashes stay. Unicode/~/+/& beyond encodeURIComponent behaviour still unverified against the service. Values are String()-coerced. Changes uncommitted; tests in test/inject.js.

