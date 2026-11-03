| Arm | Model | Traps | Runs | Pass rate (95% CI) | Last-session input tokens (median) | First request tokens (median) | Tool calls before first edit (median) |
|---|---|---|---|---|---|---|---|
| basic-memory | claude-sonnet-5-5 | 11 | 33 | 3% (0%-9%) | 128886 | 19191 | 1 |
| basic-memory (control) | claude-sonnet-5-5 | 1 | 3 | 100% (100%-100%) | 139062 | 19224 | - |
| claude-mem | claude-sonnet-5-5 | 11 | 33 | 42% (18%-67%) | 171434 | 21543 | 4 |
| claude-mem (control) | claude-sonnet-5-5 | 1 | 3 | 100% (100%-100%) | 142251 | 19403 | - |
| handoff | claude-sonnet-5-5 | 13 | 39 | 67% (41%-90%) | 133576 | 16139 | 2 |
| handoff (control) | claude-sonnet-5-5 | 1 | 3 | 100% (100%-100%) | 127145 | 16197 | - |
| hindsight | claude-sonnet-5-5 | 11 | 33 | 3% (0%-9%) | 149262 | 18692 | 4 |
| hindsight (control) | claude-sonnet-5-5 | 1 | 3 | 100% (100%-100%) | 143003 | 18377 | - |
| native | claude-sonnet-5-5 | 11 | 33 | 45% (18%-73%) | 125356 | 16663 | 3 |
| native (control) | claude-sonnet-5-5 | 1 | 3 | 100% (100%-100%) | 106421 | 16684 | - |
| none | claude-sonnet-5-5 | 24 | 72 | 26% (11%-43%) | 121728 | 15926 | 3 |
| none (control) | claude-sonnet-5-5 | 2 | 6 | 100% (100%-100%) | 129121 | 15972 | - |
| oracle-note | claude-sonnet-5-5 | 24 | 72 | 97% (92%-100%) | 119431 | 16142 | 2 |
| oracle-note (control) | claude-sonnet-5-5 | 2 | 6 | 100% (100%-100%) | 138726 | 16116 | - |
| resume | claude-sonnet-5-5 | 11 | 33 | 70% (45%-91%) | 143058 | 22521 | 1 |
| resume (control) | claude-sonnet-5-5 | 1 | 3 | 100% (100%-100%) | 121747 | 15982 | - |
| trailkeep | claude-sonnet-5-5 | 9 | 9 | 22% (0%-56%) | 124394 | 16288 | 2 |
| trailkeep@capture | claude-sonnet-5-5 | 11 | 33 | 91% (73%-100%) | 140380 | 16655 | 1 |
| trailkeep@capture (control) | claude-sonnet-5-5 | 1 | 3 | 100% (100%-100%) | 104994 | 16424 | - |

Paired difference in pass rate vs `none` (same trap and seed, non-control traps):

| Arm | Model | Pairs | Difference (95% CI) |
|---|---|---|---|
| basic-memory | claude-sonnet-5-5 | 33 | +0% (+0% to +0%) |
| claude-mem | claude-sonnet-5-5 | 33 | +39% (+12% to +67%) |
| handoff | claude-sonnet-5-5 | 39 | +49% (+26% to +74%) |
| hindsight | claude-sonnet-5-5 | 33 | +0% (+0% to +0%) |
| native | claude-sonnet-5-5 | 33 | +42% (+15% to +70%) |
| oracle-note | claude-sonnet-5-5 | 72 | +71% (+54% to +86%) |
| resume | claude-sonnet-5-5 | 33 | +67% (+39% to +91%) |
| trailkeep | claude-sonnet-5-5 | 9 | +22% (+0% to +56%) |
| trailkeep@capture | claude-sonnet-5-5 | 33 | +88% (+70% to +100%) |
