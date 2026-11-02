| Arm | Model | Traps | Runs | Pass rate (95% CI) | Last-session input tokens (median) | First request tokens (median) | Tool calls before first edit (median) |
|---|---|---|---|---|---|---|---|
| handoff | claude-sonnet-5-5 | 3 | 9 | 100% (100%-100%) | 122680 | 16157 | 2 |
| none | claude-sonnet-5-5 | 3 | 9 | 67% (0%-100%) | 138333 | 15937 | 1 |
| oracle-note | claude-sonnet-5-5 | 3 | 9 | 100% (100%-100%) | 127971 | 16137 | 2 |
| trailkeep | claude-sonnet-5-5 | 3 | 9 | 100% (100%-100%) | 151524 | 16313 | 2 |

Paired difference in pass rate vs `none` (same trap and seed, non-control traps):

| Arm | Model | Pairs | Difference (95% CI) |
|---|---|---|---|
| handoff | claude-sonnet-5-5 | 9 | +33% (+0% to +100%) |
| oracle-note | claude-sonnet-5-5 | 9 | +33% (+0% to +100%) |
| trailkeep | claude-sonnet-5-5 | 9 | +33% (+0% to +100%) |
