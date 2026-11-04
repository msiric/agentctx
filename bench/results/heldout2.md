# Held-out set 2 (2026-11-04)

Pre-registered in `PREREGISTRATION.md` (addendum) before the traps existed.
11 new blind-authored fact traps (12 written, 1 dropped by the gate; see
`gate.md`), 3 seeds, frozen versions: Claude Code 2.1.317,
claude-sonnet-5-5, trailkeep 0.5.0. Runs 41854116419, 41876995757 (trailkeep,
handoff) and 41881104226 (fresh `none`, see `DEVIATIONS.md`).

## Result

| Arm | Fact traps passed | Pass rate (95% CI) | Tokens added at session start (median) | Last-session input tokens (median) |
|---|---|---|---|---|
| **trailkeep** | 26/33 | 79% (64%–94%) | +662 | 119,084 |
| handoff | 26/33 | 79% (55%–100%) | +226 | 137,246 |
| none@rerun | 2/33 | 6% (0%–18%) | +0 | 118,244 |

Tokens added are measured against the gate's `none` cells on the same trap
and seed (same versions).

Primary hypotheses: trailkeep minus comparator, paired by trap and seed (fact traps). Holm correction across H2b-2, H1-2.

| | Comparator | Pairs | Difference (95% CI) | p (one-sided) | Holm-adjusted p | Significant at 0.05 | Trap-level p (sensitivity) |
|---|---|---|---|---|---|---|---|
| H2b-2 | handoff | 33 | +0% (-21% to +24%) | 0.6230 | 0.6230 | no | 0.5938 |
| H1-2 | none@rerun | 33 | +73% (+58% to +88%) | 0.0000 | 0.0000 | yes | 0.0005 |

- **H1-2 holds:** trailkeep beats no memory by 73 points.
- **H2b-2 does not:** trailkeep and the handoff file tie at 79%. This is not
  evidence that they are equivalent; the interval is -21 to +24 points.
- **H5:** on both superseded traps, trailkeep and handoff followed the newer
  decision 3/3; no memory failed 3/3.
- Gate-cell `none` (reference only, selected on): 1/33.

## Per trap

| Trap | trailkeep | handoff | none (fresh) |
|---|---|---|---|
| branch-isolation-fiscal-quarter | 3/3 | 3/3 | 0/3 |
| branch-isolation-semver-silent-deprecation | 1/3 | 0/3 | 0/3 |
| constraint-fork-upstream-files | 3/3 | 3/3 | 0/3 |
| cross-repo-doctest-examples | 3/3 | 3/3 | 2/3 |
| cross-repo-version-bump | 3/3 | 0/3 | 0/3 |
| dead-end-humanize-half-up | 2/3 | 2/3 | 0/3 |
| dead-end-inject-encoding | 1/3 | 3/3 | 0/3 |
| decision-schema-length-bytes | 3/3 | 3/3 | 0/3 |
| decision-week-numbering | 2/3 | 3/3 | 0/3 |
| superseded-semver-json-output | 3/3 | 3/3 | 0/3 |
| superseded-test-runner | 2/3 | 3/3 | 0/3 |

`cross-repo-doctest-examples` had little headroom (no memory passed 1/3 in
the gate, 2/3 here), which is why the handoff file passes a cross-repo trap
there.

## Failure labels

**trailkeep (7 failures):**
- **Capture miss (6):** the fact was never saved.
  - branch-isolation-semver s1, s2
  - dead-end-inject-encoding s1, s2
  - dead-end-humanize s3
  - decision-week-numbering s2

  In these runs the agent didn't call `trailkeep note` for the fact.
- **Other (1):** superseded-test-runner s3. The facts passed, but the task
  check failed on a test that was already failing, which the agent noted and
  left.

**handoff (7 failures):**
- **Retrieval miss (5):**
  - cross-repo-version-bump s1–s3: the preference was in the other repo's
    HANDOFF.md.
  - branch-isolation-semver s1, s2: the one HANDOFF.md per working tree
    didn't hold the branch's rule as a rule.
- **Use failure (2):** branch-isolation-semver s3 and dead-end-humanize s1.
  The fact was in the file, and the agent didn't follow it.

## Reading

The two approaches fail in different places:
- **The handoff file captures more reliably.** Its instruction ends with
  "Update it before you finish", so every session writes a summary.
  trailkeep relies on the agent noticing, mid-task, that something is worth
  saving. It missed 6 of 33 times.
- **trailkeep retrieves better.** It carries rules across repos and keeps
  branches apart, which a single file per working tree can't do.

Exploratory, mixing trailkeep versions: across both held-out sets (17 traps,
51 pairs), trailkeep passed 41/51 (80%) and handoff passed 37/51 (73%).
