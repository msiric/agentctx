# storage-app

Branch: storage-app · Repo: local__pretty-bytes-3571150565 · Kind: branch · Created: 2026-11-06

## Decisions and dead ends

- 2026-11-06: parseBytes (named export) supports only plain numbers/B and binary KiB..YiB, case-sensitive. kB/MB/GB etc deliberately unsupported (throw SyntaxError) until the user hears back from the storage team on how to read them. My choices: accepts optional sign/surrounding whitespace/nbsp separator; fractional bytes not rounded; throws TypeError for non-strings.
- 2026-11-06: Storage team answer: on this branch (storage-app) parseBytes must read the non-i units as powers of 1024 (Windows Explorer style): '1 KB' or '1 kB' = 1024, '1 MB' = 1048576, and so on. Not implemented yet; the user will add it next session. Until then they still throw SyntaxError. Whether other casings (e.g. 'kb') are accepted was not decided; ask.
- 2026-11-06: parseBytes now implemented: kB/KB/MB/GB.. = powers of 1024 (storage team, Windows Explorer style). My choice (not user-decided): other casings like 'kb', 'mb', 'Kb' still throw SyntaxError; only 'kB' and 'KB' accepted for kilo. Documented in readme + index.d.ts.

