| Arm | Model | Traps | Runs | Pass rate (95% CI) | Last-session input tokens (median) | First request tokens (median) | Tool calls before first edit (median) |
|---|---|---|---|---|---|---|---|
| basic-memory | claude-sonnet-5-5 | 9 | 9 | 0% (0%-0%) | 140367 | 19192 | 1 |
| claude-mem | claude-sonnet-5-5 | 9 | 9 | 44% (11%-78%) | 171434 | 21608 | 4 |
| handoff | claude-sonnet-5-5 | 11 | 17 | 88% (67%-100%) | 129893 | 16157 | 2 |
| hindsight | claude-sonnet-5-5 | 9 | 9 | 0% (0%-0%) | 149262 | 18719 | 4 |
| native | claude-sonnet-5-5 | 9 | 9 | 56% (22%-89%) | 127703 | 16752 | 3 |
| none | claude-sonnet-5-5 | 24 | 72 | 26% (11%-43%) | 121728 | 15926 | 3 |
| none (control) | claude-sonnet-5-5 | 2 | 6 | 100% (100%-100%) | 129121 | 15972 | - |
| oracle-note | claude-sonnet-5-5 | 24 | 72 | 97% (92%-100%) | 119431 | 16142 | 2 |
| oracle-note (control) | claude-sonnet-5-5 | 2 | 6 | 100% (100%-100%) | 138726 | 16116 | - |
| resume | claude-sonnet-5-5 | 9 | 9 | 67% (33%-89%) | 139391 | 23050 | 0 |
| trailkeep | claude-sonnet-5-5 | 9 | 9 | 22% (0%-56%) | 124394 | 16288 | 2 |
| trailkeep@capture | claude-sonnet-5-5 | 11 | 33 | 91% (73%-100%) | 140380 | 16655 | 1 |
| trailkeep@capture (control) | claude-sonnet-5-5 | 1 | 3 | 100% (100%-100%) | 104994 | 16424 | - |

Paired difference in pass rate vs `none` (same trap and seed, non-control traps):

| Arm | Model | Pairs | Difference (95% CI) |
|---|---|---|---|
| basic-memory | claude-sonnet-5-5 | 9 | +0% (+0% to +0%) |
| claude-mem | claude-sonnet-5-5 | 9 | +44% (+11% to +78%) |
| handoff | claude-sonnet-5-5 | 17 | +53% (+21% to +91%) |
| hindsight | claude-sonnet-5-5 | 9 | +0% (+0% to +0%) |
| native | claude-sonnet-5-5 | 9 | +56% (+22% to +89%) |
| oracle-note | claude-sonnet-5-5 | 72 | +71% (+54% to +86%) |
| resume | claude-sonnet-5-5 | 9 | +67% (+33% to +89%) |
| trailkeep | claude-sonnet-5-5 | 9 | +22% (+0% to +56%) |
| trailkeep@capture | claude-sonnet-5-5 | 33 | +88% (+70% to +100%) |
