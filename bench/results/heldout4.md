# Held-out set 4 (2026-11-06)

Pre-registered in PREREGISTRATION.md (set 4 addendum) before the traps
existed. 12 blind-authored traps, 10 kept by the gate (gate.md). trailkeep
0.5.2, `handoff` and `none@rerun`, 3 seeds, dispatched once from the frozen
branch `bench-heldout4` (run 42157735269, 90 cells, no pauses).

## Results, as pre-registered

Output of `analyze.py --plan bench/plans/heldout4.json --compare H2b-4=handoff --compare H1-4=none@rerun`.
The cell count includes the gate's cells. "Tokens added" is measured against
the gate's `none` cells on the same trap and seed.

Runs: 150 cells, 10 fact traps, 0 control traps, arms: trailkeep, handoff, none@rerun.
Versions: Claude Code 2.1.317 (Claude Code), claude-sonnet-5-5, trailkeep 7a1e076; Claude Code 2.1.317 (Claude Code), claude-sonnet-5-5, trailkeep fcae879.

| Arm | Fact traps passed | Pass rate (95% CI) | Tokens added at session start (median) | Last-session input tokens (median) | Control |
|---|---|---|---|---|---|
| **trailkeep** | 23/30 | 77% (50%–100%) | +932 | 155,066 | 0/0 |
| handoff | 21/30 | 70% (40%–100%) | +222 | 187,306 | 0/0 |
| none@rerun | 1/30 | 3% (0%–10%) | +0 | 150,642 | 0/0 |

Primary hypotheses: trailkeep minus comparator, paired by trap and seed (fact traps). Holm correction across H2b-4, H1-4.

| | Comparator | Pairs | Difference (95% CI) | p (one-sided) | Holm-adjusted p | Significant at 0.05 | Trap-level p (sensitivity) |
|---|---|---|---|---|---|---|---|
| H2b-4 | handoff | 30 | +7% (-27% to +40%) | 0.3770 | 0.3770 | no | 0.5000 |
| H1-4 | none@rerun | 30 | +73% (+47% to +93%) | 0.0000 | 0.0000 | yes | 0.0039 |

H5 (hygiene), superseded-jmespath-rounding: runs failing a fact check (the stale or the newer fact) per arm:
  - trailkeep: 0/3
  - handoff: 0/3
  - none@rerun: 3/3
H5 (hygiene), superseded-qs-new-options-default-on: runs failing a fact check (the stale or the newer fact) per arm:
  - trailkeep: 0/3
  - handoff: 0/3
  - none@rerun: 3/3

## Per trap

| Trap | trailkeep | handoff | none |
|---|---|---|---|
| branch-isolation-camelcase-release-bump | 3/3 | 0/3 | 0/3 |
| branch-tabulate-missing-marker | 3/3 | 3/3 | 0/3 |
| constraint-pretry-generated-dts | 3/3 | 3/3 | 1/3 |
| constraint-sqlparse-keywords-frozen | 0/3 (3/3 re-scored) | 3/3 | 0/3 |
| dead-end-qs-json-bigint | 0/3 | 0/3 | 0/3 |
| deadend-tabulate-wrap-splits-tokens | 3/3 | 3/3 | 0/3 |
| decision-pretry-retry-after-additive | 2/3 | 3/3 | 0/3 |
| superseded-jmespath-rounding | 3/3 | 3/3 | 0/3 |
| superseded-qs-new-options-default-on | 3/3 | 3/3 | 0/3 |
| xrepo-doctest-examples | 3/3 | 0/3 | 0/3 |

## Failure labels

trailkeep, 7 failures as recorded:

- constraint-sqlparse-keywords-frozen s1–s3: check broken (DEVIATIONS.md,
  2026-11-06). The fact was honoured and the code passes in a clean
  environment. The runs followed the repo's AGENTS.md and used uv, which
  breaks the check's pytest.
- dead-end-qs-json-bigint s1, s2: use failure. The notes recorded the 64-bit
  dead end. The last session stopped to ask how to handle big integers
  instead of building the feature.
- dead-end-qs-json-bigint s3: use failure. It recalled the dead end and built
  plain JSON.parse anyway, noting the precision issue as open.
- decision-pretry-retry-after-additive s2: use failure. The note held the
  user's decision (Retry-After plus backoff). Session 2's notes listed the
  agent's own open design points as "my recommendations, not user
  decisions", and the last session didn't add Retry-After to the backoff.

handoff, 9 failures:

- branch-isolation-camelcase-release-bump s1–s3: the patch-bump rule from the
  release branch's session was lost (one HANDOFF.md per worktree, rewritten
  on the other branch).
- xrepo-doctest-examples s1–s3: retrieval miss, the preference was in the
  other repo's HANDOFF.md.
- dead-end-qs-json-bigint s1–s3: built plain JSON.parse.

## Sensitivity analyses

| | trailkeep | handoff | Difference (95% CI) | p (one-sided) | Trap-level p |
|---|---|---|---|---|---|
| As recorded (primary) | 23/30 | 21/30 | +7% (−27% to +40%) | 0.377 | 0.50 |
| sqlparse re-scored | 26/30 | 21/30 | +17% (−7% to +47%) | 0.063 | 0.25 |
| As recorded, without the 2 traps that resemble set 2 | 17/24 | 18/24 | −4% (−42% to +33%) | 0.773 | 0.75 |
| Re-scored, without those 2 traps | 20/24 | 18/24 | +8% (−12% to +38%) | 0.313 | 0.50 |

## Reading

- H1-4 holds: trailkeep beats no memory by 73 points (p < 0.0001).
- H2b-4 is not supported: +7 points over handoff, p = 0.38. Re-scoring the
  broken check gives +17 points, p = 0.06, still not significant.
- Same pattern as sets 2 and 3. Handoff loses where a fact lives in another
  repo or on another branch. trailkeep loses on single-repo facts it had
  but didn't act on.
- Possible side effect of 0.5.2, not tested: three of trailkeep's four real
  failures stopped short of the user's instruction after notes split "user
  decided" from "my recommendation" or listed open options. Marking the
  agent's own choices may make the next session wait for confirmation.

## Exploratory: all four held-out sets pooled

Mixes trailkeep versions (0.4.0 to 0.5.2) and was not pre-registered. 39
traps, 117 pairs:

| | trailkeep | handoff | Difference (95% CI) | p (one-sided) | Trap-level p |
|---|---|---|---|---|---|
| As recorded | 96/117 (82%) | 86/117 (74%) | +9% (−6% to +23%) | 0.066 | 0.15 |
| sqlparse re-scored | 99/117 (85%) | 86/117 (74%) | +11% (−2% to +25%) | 0.018 | 0.07 |

The re-scored pooled p is below 0.05 at the run level but not at the trap
level, and both the pooling and the re-scoring were chosen after seeing the
data. It is a hint, not a confirmed result.
