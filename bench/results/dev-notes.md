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

## 3. Dev matrix complete (2026-11-03)

All arms, 11 dev fact traps × 3 seeds (trailkeep v0.3.2: seed 1 only), plus
the dev control. Pass rate with 95% cluster-bootstrap CI over traps:

| Arm | Fact traps | vs none (paired) | vs handoff (paired) | Session-start tokens (median) | Control |
|---|---|---|---|---|---|
| oracle-note | 100% (100–100) | +97% | +39% (+15 to +67) | 16,134 | 3/3 |
| **trailkeep@capture** | **91% (73–100)** | **+88% (+67 to +100)** | **+30% (+6 to +55)** | **16,655** | 3/3 |
| resume | 70% (45–91) | +67% | +9% (−30 to +45) | 22,521 | 3/3 |
| handoff | 61% (33–85) | +58% (+33 to +82) | — | 16,139 | 3/3 |
| native | 45% (18–73) | +42% | −15% (−36 to 0) | 16,663 | 3/3 |
| claude-mem | 42% (18–67) | +39% | −18% (−45 to +3) | 21,543 | 3/3 |
| trailkeep v0.3.2 | 22% (0–56), 9 runs | +22% | −56% | 16,288 | – |
| hindsight | 3% (0–9) | 0% | −58% | 18,692 | 3/3 |
| basic-memory | 3% (0–9) | 0% | −58% | 19,191 | 3/3 |
| none | 3% (0–9) | — | −58% | 15,924 | 3/3 |

No arm hurt the control (H4 holds in dev). `none`'s session-start request is
15,924 tokens; trailkeep@capture adds about 730, handoff about 215, claude-mem
about 5,600, resume about 6,600.

**Handoff's 13 failures**, the strongest competitor:
- 9 cross-repo (both cross-repo traps, every seed): the preference was written
  to the first repo's `HANDOFF.md`, which the second repo never sees.
  Retrieval miss by design; a per-repo file can't carry a personal preference.
- 4 dead-end: the dead end was in `HANDOFF.md` and the last session read it,
  but retried the approach anyway (use failure).

**trailkeep@capture's 3 failures:** one trap, use failure (section 2).

H3 (lean) in dev: session-start cost is within budget (+730 tokens, far under
2,500). The last session's total input is higher than `none`'s (140k vs
105k), so the second half of H3 doesn't hold in dev; `none` mostly takes the
trap's shortcut and stops sooner, so this compares unequal work.

## Next: held-out run

Freeze trailkeep at the `trailkeep@capture` commit (released as 0.4.0) and
every other tool at the versions recorded in the dev cells, size the filler
arm from trailkeep's measured injection, and run the 6 held-out fact traps
plus the held-out control once, all arms, 3 seeds.

## 4. Correction: Hindsight's dev results are invalid (2026-11-03)

Hindsight's memory extraction failed in every dev cell: its LLM provider
defaulted to a model that is no longer served, so it stored nothing from the
conversations (see `DEVIATIONS.md`). Its 3% in the tables above measures a
broken setup, not Hindsight. With the model set explicitly it stores
memories again (one-episode smoke check, which passed). Its held-out cells
run with the fix.

## 5. Changes after the held-out run (toward 0.5.0)

From the held-out failure labels (`heldout.md`):
- **Scope:** on a branch with no notes yet, trailkeep now shows up to 5
  recent decisions from other branches (from their effort files in the
  worktree, then the log), each labelled with its branch. A branch with its
  own notes sees only those. Risk: branch-isolation traps, where another
  branch's rule must not apply; checked by the dev re-run.
- **Capture rule:** names the three scopes explicitly, with `--repo` for rules
  about the codebase.
- **Framing:** injected notes are headed as rules/decisions to follow unless
  the user says otherwise.

Validated on the dev traps as arm `trailkeep@scope` (plan `dev-scope`). The
held-out traps are no longer unseen, so they aren't used to tune this; a
fresh held-out set comes next.

## 6. `trailkeep@scope` on the dev traps: 31 of 33 (2026-11-04)

Run 41819878467, pinned versions, 12 dev traps × 3 seeds.

| | `trailkeep@capture` (0.4.0) | `trailkeep@scope` |
|---|---|---|
| Fact traps passed | 30/33 (91%) | 31/33 (94%) |
| Branch-isolation traps | 6/6 | 6/6 |
| xrepo-error-prefix | 0/3 | 2/3 |
| deadend-sortkeys | 3/3 | 2/3 |
| Control | 3/3 | 3/3 |

No regression on branch isolation: the other-branch list only appears on a
branch with no notes, and both branch traps' last sessions had their own.

Failures, both **use failures** (the note was captured and injected in the
last session):
- xrepo-error-prefix s1: the `--all` note was injected under the new
  "preferences for every repo" heading; the agent still wrote an unprefixed
  message. The note carried a qualifier ("applied to new messages only in
  pretty-bytes") that may have read as narrowing it.
- deadend-sortkeys s1: the dead end was injected; the agent chose a
  different fix (fall back to unsorted) than the one the checker requires.

Bug found: agents sometimes write their own date, giving
"2026-11-04: 2026-11-04: ...". `note` now drops a leading date.

Small sample (one seed per difference); read as "no regression", not as an
improvement. Released as 0.5.0.
