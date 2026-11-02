| Arm | Model | Traps | Runs | Pass rate (95% CI) | Last-session input tokens (median) | First request tokens (median) | Tool calls before first edit (median) |
|---|---|---|---|---|---|---|---|
| basic-memory | claude-sonnet-5-5 | 9 | 9 | 0% (0%-0%) | 140367 | 19192 | 1 |
| claude-mem | claude-sonnet-5-5 | 9 | 9 | 44% (11%-78%) | 171434 | 21608 | 4 |
| handoff | claude-sonnet-5-5 | 10 | 16 | 88% (64%-100%) | 131734 | 16157 | 2 |
| hindsight | claude-sonnet-5-5 | 9 | 9 | 0% (0%-0%) | 149262 | 18719 | 4 |
| native | claude-sonnet-5-5 | 9 | 9 | 56% (22%-89%) | 127703 | 16752 | 3 |
| none | claude-sonnet-5-5 | 24 | 72 | 26% (11%-43%) | 121728 | 15926 | 3 |
| none (control) | claude-sonnet-5-5 | 2 | 6 | 100% (100%-100%) | 129121 | 15972 | - |
| oracle-note | claude-sonnet-5-5 | 24 | 72 | 97% (92%-100%) | 119431 | 16142 | 2 |
| oracle-note (control) | claude-sonnet-5-5 | 2 | 6 | 100% (100%-100%) | 138726 | 16116 | - |
| resume | claude-sonnet-5-5 | 8 | 8 | 62% (25%-88%) | 148619 | 22910 | 0 |
| trailkeep | claude-sonnet-5-5 | 8 | 8 | 12% (0%-38%) | 133586 | 16287 | 2 |

Paired difference in pass rate vs `none` (same trap and seed, non-control traps):

| Arm | Model | Pairs | Difference (95% CI) |
|---|---|---|---|
| basic-memory | claude-sonnet-5-5 | 9 | +0% (+0% to +0%) |
| claude-mem | claude-sonnet-5-5 | 9 | +44% (+11% to +78%) |
| handoff | claude-sonnet-5-5 | 16 | +50% (+19% to +90%) |
| hindsight | claude-sonnet-5-5 | 9 | +0% (+0% to +0%) |
| native | claude-sonnet-5-5 | 9 | +56% (+22% to +89%) |
| oracle-note | claude-sonnet-5-5 | 72 | +71% (+54% to +86%) |
| resume | claude-sonnet-5-5 | 8 | +62% (+25% to +88%) |
| trailkeep | claude-sonnet-5-5 | 8 | +12% (+0% to +38%) |
