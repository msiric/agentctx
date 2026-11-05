# Held-out set 3 (2026-11-05)

Pre-registered in PREREGISTRATION.md (set 3 addendum) before the traps
existed. 12 blind-authored traps, all kept by the gate (gate.md). trailkeep
0.5.1, `handoff` and `none@rerun`, 3 seeds, dispatched once from the frozen
branch `bench-heldout3` (run 42035632490, 108 cells, no pauses).

## Results

Output of `analyze.py --plan bench/plans/heldout3.json --compare H2b-3=handoff --compare H1-3=none@rerun`.
The cell count includes the gate's cells for these traps. "Tokens added" is
measured against the gate's `none` cells on the same trap and seed.

Runs: 180 cells, 12 fact traps, 0 control traps, arms: trailkeep, handoff, none@rerun.
Versions: Claude Code 2.1.317 (Claude Code), claude-sonnet-5-5, trailkeep a4435b5; Claude Code 2.1.317 (Claude Code), claude-sonnet-5-5, trailkeep d44133a.

| Arm | Fact traps passed | Pass rate (95% CI) | Tokens added at session start (median) | Last-session input tokens (median) | Control |
|---|---|---|---|---|---|
| **trailkeep** | 32/36 | 89% (75%–100%) | +866 | 134,111 | 0/0 |
| handoff | 28/36 | 78% (53%–100%) | +220 | 132,910 | 0/0 |
| none@rerun | 0/36 | 0% (0%–0%) | +0 | 102,556 | 0/0 |

Primary hypotheses: trailkeep minus comparator, paired by trap and seed (fact traps). Holm correction across H2b-3, H1-3.

| | Comparator | Pairs | Difference (95% CI) | p (one-sided) | Holm-adjusted p | Significant at 0.05 | Trap-level p (sensitivity) |
|---|---|---|---|---|---|---|---|
| H2b-3 | handoff | 36 | +11% (-8% to +36%) | 0.1719 | 0.1719 | no | 0.2500 |
| H1-3 | none@rerun | 36 | +89% (+75% to +100%) | 0.0000 | 0.0000 | yes | 0.0002 |

H5 (hygiene), superseded-none-values: runs failing a fact check (the stale or the newer fact) per arm:
  - trailkeep: 0/3
  - handoff: 0/3
  - none@rerun: 3/3
H5 (hygiene), superseded-range-size-no-throw: runs failing a fact check (the stale or the newer fact) per arm:
  - trailkeep: 1/3
  - handoff: 0/3
  - none@rerun: 3/3

## Per trap

| Trap | trailkeep | handoff | none |
|---|---|---|---|
| branch-isolation-bytes-rounding | 1/3 | 1/3 | 0/3 |
| branch-isolation-sort-default | 3/3 | 3/3 | 0/3 |
| constraint-bytes-no-regex | 3/3 | 3/3 | 0/3 |
| constraint-no-runtime-warnings | 3/3 | 3/3 | 0/3 |
| cross-repo-error-prefix | 3/3 | 0/3 | 0/3 |
| cross-repo-keyword-only-options | 3/3 | 0/3 | 0/3 |
| dead-end-bytes-decimal-float | 3/3 | 3/3 | 0/3 |
| dead-end-deep-documents | 2/3 | 3/3 | 0/3 |
| decision-flatten-separator | 3/3 | 3/3 | 0/3 |
| decision-range-limit-coalesce | 3/3 | 3/3 | 0/3 |
| superseded-none-values | 3/3 | 3/3 | 0/3 |
| superseded-range-size-no-throw | 2/3 | 3/3 | 0/3 |

Without cross-repo-error-prefix (see gate.md): trailkeep 29/33, handoff
28/33, none 0/33.

## Failure labels

trailkeep, 4 failures:

- branch-isolation-bytes-rounding s1, s2: use failure. Both runs had the
  billing branch's rule (never show more than was used). Both built it as an
  opt-in option and left the default rounding up, so the billing output still
  rounds up. In s1 an agent-written repo note ("don't change the default
  rounding; add a per-call option") pushed that way.
- dead-end-deep-documents s2: capture miss. The note recorded drop_keys's
  design but not the RecursionError on deep catalogs.
- superseded-range-size-no-throw s2: use failure. The note said not to throw.
  The last session read "the change is deferred" as "keep throwing" and
  extended the throw.

handoff, 8 failures:

- cross-repo-error-prefix s1–s3, cross-repo-keyword-only-options s1–s3:
  retrieval miss. The preference was in the other repo's HANDOFF.md.
- branch-isolation-bytes-rounding s3: use failure, the same opt-in pattern as
  trailkeep's.
- branch-isolation-bytes-rounding s1: other. Both facts honoured; the task's
  expected '1.2MB' came out as '1.19MB'.

## Reading

- H1-3 holds: trailkeep beats no memory by 89 points (p < 0.0001).
- H2b-3 is not supported: +11 points over handoff (95% CI −8 to +36),
  p = 0.17. Without the trap that resembles a dev trap it is +3 points.
- The pattern matches set 2. Handoff loses only where a fact lives in
  another repo, which it has no channel for. trailkeep loses on single-repo
  facts it misused or, once, didn't record.
- The capture fix held: 1 capture miss in 36 runs, against 6 in 33 on set 2.

## Exploratory: all three held-out sets pooled

Mixes trailkeep versions (0.4.0, 0.5.0, 0.5.1), so it is not a test of any
one version. 29 traps, 87 pairs:

| | trailkeep | handoff | Difference (95% CI) | p (one-sided) | Trap-level p |
|---|---|---|---|---|---|
| Pooled | 73/87 (84%) | 65/87 (75%) | +9% (−6% to +25%) | 0.085 | 0.16 |
