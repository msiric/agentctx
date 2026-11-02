| Arm | Model | Traps | Runs | Pass rate (95% CI) | Last-session input tokens (median) | First request tokens (median) | Tool calls before first edit (median) |
|---|---|---|---|---|---|---|---|
| basic-memory | claude-sonnet-5-5 | 1 | 1 | 0% (0%-0%) | 80136 | 19118 | - |
| claude-mem | claude-sonnet-5-5 | 1 | 1 | 0% (0%-0%) | 91194 | 20697 | - |
| handoff | claude-sonnet-5-5 | 3 | 9 | 100% (100%-100%) | 122680 | 16157 | 2 |
| hindsight | claude-sonnet-5-5 | 1 | 1 | 100% (100%-100%) | 184851 | 18650 | 4 |
| none | claude-sonnet-5-5 | 24 | 72 | 26% (11%-43%) | 121728 | 15926 | 3 |
| none (control) | claude-sonnet-5-5 | 2 | 6 | 100% (100%-100%) | 129121 | 15972 | - |
| oracle-note | claude-sonnet-5-5 | 24 | 72 | 97% (92%-100%) | 119431 | 16142 | 2 |
| oracle-note (control) | claude-sonnet-5-5 | 2 | 6 | 100% (100%-100%) | 138726 | 16116 | - |
| trailkeep | claude-sonnet-5-5 | 3 | 9 | 100% (100%-100%) | 151524 | 16313 | 2 |

Paired difference in pass rate vs `none` (same trap and seed, non-control traps):

| Arm | Model | Pairs | Difference (95% CI) |
|---|---|---|---|
| basic-memory | claude-sonnet-5-5 | 1 | +0% (+0% to +0%) |
| claude-mem | claude-sonnet-5-5 | 1 | +0% (+0% to +0%) |
| handoff | claude-sonnet-5-5 | 9 | +33% (+0% to +100%) |
| hindsight | claude-sonnet-5-5 | 1 | +100% (+100% to +100%) |
| oracle-note | claude-sonnet-5-5 | 72 | +71% (+54% to +86%) |
| trailkeep | claude-sonnet-5-5 | 9 | +33% (+0% to +100%) |
