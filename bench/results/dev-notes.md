# Dev matrix notes (exploratory, dev traps only)

Nothing here is a finding: findings come from the held-out run. These notes
record what the dev results showed and what was changed because of them.

## 1. trailkeep v0.3.2 barely captured anything (2026-11-03)

After the first dev batch (seed 1, 59 new cells), fact traps passed:

| Arm | Passed |
|---|---|
| oracle-note | 33/33 |
| handoff | 8/10 |
| native | 5/9 |
| resume | 5/8 |
| claude-mem | 4/9 |
| trailkeep | 1/8 |
| none | 1/33 |
| basic-memory | 0/9 |
| hindsight | 0/9 |

Failure labels for trailkeep's 7 failures: **7 capture misses**. In every one
nothing was written: no effort file, no notes, no log lines. The only pass
was the trap where the user says "for next time", which the agent took as a
cue to create an effort file.

Why: v0.3.2 only asked for capture through a hint on non-default branches
("If this task spans more than one session, run `trailkeep new`"). The agent
can't know a task spans sessions, so it never acts, and on the default branch
there was no hint at all. The handoff arm, one standing instruction to keep a
file current, did far better with the same model.

## Change: a standing capture rule and `trailkeep note`

- Every session in a repo now gets one short rule (about 110 tokens): record
  a decision and its reason, a user rule or preference, or a failed approach
  the moment it comes up, with `trailkeep note "<what and why>"`.
- `trailkeep note` appends a dated line to the branch's effort file, creating
  a notes-only file if there is none (injected without empty Goal/Plan
  sections). `--repo` writes the repo's private notes; `--all` writes
  `~/.agents/NOTES.md`, injected in every repo, never the user's own
  `AGENTS.md`.
- Dated dead-end lines are now typed `dead-end` in the log.

The new version runs as arm `trailkeep@capture` (plan `dev-capture`) on the
same dev traps. The v0.3.2 cells keep running to completion from the frozen
branch `bench-v0.3.2`, so the before and after are both measured in full.
