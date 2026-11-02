# Trap specification

A trap is a short multi-session coding episode. Earlier sessions surface a
fact that the last session needs and that the code alone doesn't reveal. A
hidden check scores the last session. The harness runs every trap
identically under each memory condition being compared. The trap itself
knows nothing about any memory tool.

## Layout

```
traps/<id>/
  trap.json           the episode (schema below)
  setup.sh            optional: runs in each repo after checkout (install deps, create branches)
  oracle/check.sh     hidden scorer, run in the primary repo after the last session
  oracle/...          anything check.sh needs (hidden tests, fixtures)
  reference/good.patch   a final state that honours every fact
  reference/trap.patch   a plausible final state that violates the trap's key fact
```

`oracle/` and `reference/` are never copied where the agent can see them.

## trap.json

```json
{
  "id": "decision-cache-backend",
  "family": "decision",
  "summary": "For humans only, never shown to the agent: what the trap tests.",
  "repos": [
    { "name": "app", "url": "https://github.com/OWNER/REPO", "commit": "<full sha>" }
  ],
  "sessions": [
    { "repo": "app", "branch": "feature/cache", "turns": ["...", "..."] },
    { "repo": "app", "branch": "feature/cache", "turns": ["..."] }
  ],
  "facts": [
    { "id": "f1", "text": "Use the file cache, not Redis: deploy target has no Redis.",
      "source": "user", "session": 1, "superseded_by": null }
  ],
  "budget": { "max_turns_per_session": 60 }
}
```

- **families:** `decision`, `dead-end`, `constraint`, `superseded`,
  `branch-isolation`, `cross-repo-preference`, `control`.
- **sessions:** run in order, each one a fresh agent process. `turns` are the
  user's messages, sent one at a time; each waits for the agent to finish.
  The harness appends one fixed closing message to every session ("That's all
  for today, thanks."). Don't write a closing message yourself.
- **The last session's first turn** must be neutral, like a real user picking
  work back up: "Let's carry on with the export feature." It must not restate,
  hint at or paraphrase any fact.
- **facts:** everything the last session must respect.
  - `source: "user"`: the user states it in a turn.
  - `source: "discovered"`: the agent learns it by doing something in an
    earlier session, for example running a command that fails in a
    revealing way.
  - `superseded_by` names a later fact that replaces this one.
- **repos:** public, permissively licensed (MIT, BSD, Apache-2.0), small
  (under ~20k lines), with tests that run offline in under a minute after
  setup. Pin a full commit SHA. A `cross-repo-preference` trap uses two repos.

## Branches

Before each session the harness checks out that session's `branch` in its
repo, creating it from the pinned commit if it doesn't exist yet. Work left
uncommitted by one session stays in the working tree for the next, as on a
real machine.

## oracle/check.sh

- Runs with the last session's repo (the primary repo) as the current
  directory, on its final working tree.
  It may read `git log` and `git diff` too.
- Exit 0 means the last session succeeded at the task *and* respected the
  facts. Any other exit means fail.
- On stdout, print one JSON object per line with a pass or fail for each
  fact, e.g. `{"fact": "f1", "ok": false, "why": "imports redis"}`, plus one
  `{"task": true}` line for the task itself.
- Deterministic and offline. Use no LLM and no network.

## Validity, checked before a trap is accepted

1. `check.sh` fails on the starting state (after the scripted earlier
   sessions are *not* run).
2. It passes with `reference/good.patch` applied.
3. It fails with `reference/trap.patch` applied. This patch is the natural
   thing a capable agent does without the fact, and is also a correct-looking
   solution of the task.
4. The fact can't be recovered from the repo at the start of the last session
   unless an earlier session wrote it down. Not in the code, docs, tests,
   commit messages or issue text.

## Scale

- 2 to 4 sessions, at most 4 user turns each.
- Each session is something an agent finishes in roughly 10 to 40 tool calls.
- Prefer facts a real team would have:
  - a reason a library was ruled out
  - a production constraint
  - a reviewer's preference
  - a migration that already failed
  - a test that is flaky for a known reason
  - a decision that was later reversed

## Families

| Family | Earlier sessions | Last session tests |
|---|---|---|
| decision | a choice between two reasonable options is made, with a reason | keeps the chosen option where the other is more natural |
| dead-end | an approach is tried and fails, for a non-obvious reason | doesn't retry it |
| constraint | the user sets a rule ("don't change the public API of X") | the rule holds while the task tempts breaking it |
| superseded | a decision is made, then reversed in a later session | follows the newer one |
| branch-isolation | two branches with different, conflicting facts | uses only the current branch's facts |
| cross-repo-preference | the user states a personal preference in repo A | applies it in repo B |
| control | a single session; nothing to remember | measures overhead only |
