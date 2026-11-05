# feature/options-check

Branch: feature/options-check · Repo: local__pretty-ms-3944096206 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: My choices (not user-specified): prettyMilliseconds throws TypeError for any non-undefined, non-object options, including null; arrays still pass. Reason: catch prettyMilliseconds(ms, 2) mistakes for unitCount. Changes are uncommitted; index.d.ts and readme not updated.

