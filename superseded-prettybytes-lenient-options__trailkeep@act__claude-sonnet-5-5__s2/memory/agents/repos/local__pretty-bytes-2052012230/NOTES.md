# Private notes: local__pretty-bytes-2052012230

- 2026-11-06: prettyBytes complexity lint (xo max 20) is tight: put new option validation in small helpers like forcedExponentOf instead of inlining in prettyBytes. Readme examples with // => markers are executed by the 'documented examples' test, so keep them accurate. (My choice, not a user rule.)
- 2026-11-06: User rule (2026-11-06): new options must NEVER throw on a bad value; ignore it and format as if the option wasn't passed. Reason: saved user display prefs are fed straight into prettyBytes and the shipped throw in `unit` (e.g. unit: 'KB') crashed the whole dashboard file table. `unit` already shipped with the throw, so leave it alone until the next major (then make it ignore bad values).
