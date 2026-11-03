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

## 2. trailkeep with the capture rule: 30 of 33 (2026-11-03)

Plan `dev-capture`, arm `trailkeep@capture` (commit b58ffd7), 11 dev fact
traps × 3 seeds: **30/33 passed**, controls 3/3. Other arms at this point
(mostly 1 seed each; they are still running):

| Arm | Fact traps passed | Tokens added at session start (median, vs none) |
|---|---|---|
| oracle-note | 33/33 | +210 |
| **trailkeep@capture** | **30/33** | **+730** |
| handoff | 9/11 | +210 |
| resume | 6/9 | +7,100 |
| native | 5/9 | +830 |
| claude-mem | 4/9 | +5,700 |
| trailkeep v0.3.2 | 2/9 | +360 |
| none | 1/33 | 0 |
| basic-memory | 0/9 | +3,300 |
| hindsight | 0/9 | +2,800 |

The second column is the first request's input tokens in the last session,
minus `none`'s median: everything the tool put in front of the agent before
its first step.

What was captured: in every trap the agent wrote the fact as a dated line,
with its reason, to the right scope. Branch facts went to that branch's file
(both branches of each branch-isolation trap got their own, conflicting
note), personal preferences to `~/.agents/NOTES.md`, a repo-wide convention to
the repo notes. Superseded decisions were recorded as reversals
("REVERSES earlier ...").

Failures: all 3 are `xrepo-error-prefix-prettybytes-to-cookie`, labelled
**use failure**. The preference ("error messages start with
'<package-name>: '") was captured and injected in the cookie repo, but the
agent followed cookie's existing message style instead. The note also said
"in pretty-bytes only the new error has it so far; existing messages were
left alone", which may have read as permission to skip it. Possible change:
inject personal notes as preferences to apply, not just "notes". Not made
yet; one trap is thin evidence.

Open point for H3: the last session's total input tokens are higher with
trailkeep@capture (median 140k) than with none (105k) or oracle-note (118k).
Some of that is the agent doing the full task correctly instead of the
trap's shortcut; the rest needs a look once all arms have 3 seeds.

### Update after the second phase-A batch (2026-11-03 06:30 UTC)

Other arms now have seed 1 complete and most of seed 2. Fact traps passed:

| Arm | All seeds so far | Seed 1 only |
|---|---|---|
| oracle-note | 33/33 (100%) | 11/11 |
| trailkeep@capture | 30/33 (91%) | 10/11 |
| handoff | 13/20 (65%) | 7/11 |
| resume | 12/19 (63%) | 8/11 |
| native | 8/18 (44%) | 5/11 |
| claude-mem | 8/19 (42%) | 4/11 |
| hindsight | 1/19 (5%) | 0/11 |
| basic-memory | 0/19 (0%) | 0/11 |
| none | 1/33 (3%) | 0/11 |

Session-start cost is unchanged from the table above. Phase A has 96 cells
left (seeds 2 and 3); the next batch is running.
