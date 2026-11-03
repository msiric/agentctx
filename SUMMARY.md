| Arm | Model | Traps | Runs | Pass rate (95% CI) | Last-session input tokens (median) | First request tokens (median) | Tool calls before first edit (median) |
|---|---|---|---|---|---|---|---|
| basic-memory | claude-sonnet-5-5 | 11 | 19 | 0% (0%-0%) | 132990 | 19191 | 1 |
| basic-memory (control) | claude-sonnet-5-5 | 1 | 1 | 100% (100%-100%) | 139062 | 19232 | - |
| claude-mem | claude-sonnet-5-5 | 11 | 19 | 42% (15%-71%) | 171434 | 21608 | 3 |
| claude-mem (control) | claude-sonnet-5-5 | 1 | 1 | 100% (100%-100%) | 142251 | 19403 | - |
| handoff | claude-sonnet-5-5 | 13 | 26 | 73% (48%-93%) | 131734 | 16152 | 2 |
| handoff (control) | claude-sonnet-5-5 | 1 | 1 | 100% (100%-100%) | 127145 | 16197 | - |
| hindsight | claude-sonnet-5-5 | 11 | 19 | 5% (0%-17%) | 149036 | 18717 | 4 |
| hindsight (control) | claude-sonnet-5-5 | 1 | 1 | 100% (100%-100%) | 143003 | 18493 | - |
| native | claude-sonnet-5-5 | 11 | 18 | 44% (16%-75%) | 129211 | 16662 | 3 |
| native (control) | claude-sonnet-5-5 | 1 | 1 | 100% (100%-100%) | 106421 | 16682 | - |
| none | claude-sonnet-5-5 | 24 | 72 | 26% (11%-43%) | 121728 | 15926 | 3 |
| none (control) | claude-sonnet-5-5 | 2 | 6 | 100% (100%-100%) | 129121 | 15972 | - |
| oracle-note | claude-sonnet-5-5 | 24 | 72 | 97% (92%-100%) | 119431 | 16142 | 2 |
| oracle-note (control) | claude-sonnet-5-5 | 2 | 6 | 100% (100%-100%) | 138726 | 16116 | - |
| resume | claude-sonnet-5-5 | 11 | 19 | 63% (33%-89%) | 157847 | 22521 | 0 |
| resume (control) | claude-sonnet-5-5 | 1 | 1 | 100% (100%-100%) | 125360 | 15981 | - |
| trailkeep | claude-sonnet-5-5 | 9 | 9 | 22% (0%-56%) | 124394 | 16288 | 2 |
| trailkeep@capture | claude-sonnet-5-5 | 11 | 33 | 91% (73%-100%) | 140380 | 16655 | 1 |
| trailkeep@capture (control) | claude-sonnet-5-5 | 1 | 3 | 100% (100%-100%) | 104994 | 16424 | - |

Paired difference in pass rate vs `none` (same trap and seed, non-control traps):

| Arm | Model | Pairs | Difference (95% CI) |
|---|---|---|---|
| basic-memory | claude-sonnet-5-5 | 19 | -5% (-16% to +0%) |
| claude-mem | claude-sonnet-5-5 | 19 | +37% (+5% to +70%) |
| handoff | claude-sonnet-5-5 | 26 | +46% (+20% to +73%) |
| hindsight | claude-sonnet-5-5 | 19 | +0% (+0% to +0%) |
| native | claude-sonnet-5-5 | 18 | +39% (+12% to +68%) |
| oracle-note | claude-sonnet-5-5 | 72 | +71% (+54% to +86%) |
| resume | claude-sonnet-5-5 | 19 | +58% (+23% to +89%) |
| trailkeep | claude-sonnet-5-5 | 9 | +22% (+0% to +56%) |
| trailkeep@capture | claude-sonnet-5-5 | 33 | +88% (+70% to +100%) |
