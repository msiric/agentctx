---
name: parse-compound-published
description: parseCompound shipped in 4.1.0-canary.1 and is used by the dashboard team; its behavior must stay backward compatible
metadata:
  node_type: memory
  type: project
  originSessionId: 5795ae40-e9c6-4e0c-9611-294530b269de
  modified: 2026-11-02T21:51:11.087Z
---

`parseCompound` was published in `4.1.0-canary.1` and the dashboard team already uses it. Changes to it must be backward compatible (e.g. the comma-separator support only widened accepted input), and it keeps throwing `TypeError` on bad input. Later helpers follow [[new-helpers-return-undefined]].
