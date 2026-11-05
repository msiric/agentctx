# feature/options-check

Branch: feature/options-check · Repo: local__pretty-ms-1400437634 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: prettyMilliseconds throws TypeError when options is not undefined/object; null also throws (counted as not an object, a small behaviour change from before). Reason: people pass a number like 2 thinking it is unitCount and it was silently ignored. index.d.ts and readme not updated.

