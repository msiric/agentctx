---
name: parse-compound-published
description: parseCompound shipped in 4.1.0-canary.1 and is in use; its behavior is a compatibility surface
metadata:
  node_type: memory
  type: project
  originSessionId: 5b444b4a-0fe4-4e8f-992b-295cda3663d5
  modified: 2026-11-03T05:06:39.409Z
---

`parseCompound` was released in 4.1.0-canary.1 and the dashboard team already uses it. Changes must stay backward compatible (the comma-separator follow-up on 2026-11-03 only widened accepted input). It throws TypeError on bad input; that stays. See [[new-helpers-return-undefined]].
