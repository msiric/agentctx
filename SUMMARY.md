| Arm | Model | Traps | Runs | Pass rate (95% CI) | Last-session input tokens (median) | First request tokens (median) | Tool calls before first edit (median) |
|---|---|---|---|---|---|---|---|
| basic-memory | claude-sonnet-5-5 | 11 | 29 | 3% (0%-10%) | 125415 | 19192 | 1 |
| basic-memory (control) | claude-sonnet-5-5 | 1 | 2 | 100% (100%-100%) | 147937 | 18551 | - |
| claude-mem | claude-sonnet-5-5 | 11 | 28 | 39% (17%-65%) | 176428 | 21493 | 4 |
| claude-mem (control) | claude-sonnet-5-5 | 1 | 2 | 100% (100%-100%) | 141126 | 19404 | - |
| handoff | claude-sonnet-5-5 | 13 | 35 | 69% (44%-89%) | 133576 | 16143 | 2 |
| handoff (control) | claude-sonnet-5-5 | 1 | 2 | 100% (100%-100%) | 125152 | 16198 | - |
| hindsight | claude-sonnet-5-5 | 11 | 29 | 3% (0%-10%) | 149036 | 18692 | 4 |
| hindsight (control) | claude-sonnet-5-5 | 1 | 2 | 100% (100%-100%) | 151280 | 18435 | - |
| native | claude-sonnet-5-5 | 11 | 29 | 45% (16%-75%) | 125773 | 16663 | 3 |
| native (control) | claude-sonnet-5-5 | 1 | 2 | 100% (100%-100%) | 115457 | 16683 | - |
| none | claude-sonnet-5-5 | 24 | 72 | 26% (11%-43%) | 121728 | 15926 | 3 |
| none (control) | claude-sonnet-5-5 | 2 | 6 | 100% (100%-100%) | 129121 | 15972 | - |
| oracle-note | claude-sonnet-5-5 | 24 | 72 | 97% (92%-100%) | 119431 | 16142 | 2 |
| oracle-note (control) | claude-sonnet-5-5 | 2 | 6 | 100% (100%-100%) | 138726 | 16116 | - |
| resume | claude-sonnet-5-5 | 11 | 28 | 64% (39%-88%) | 141224 | 22578 | 1 |
| resume (control) | claude-sonnet-5-5 | 1 | 2 | 100% (100%-100%) | 123554 | 15982 | - |
| trailkeep | claude-sonnet-5-5 | 9 | 9 | 22% (0%-56%) | 124394 | 16288 | 2 |
| trailkeep@capture | claude-sonnet-5-5 | 11 | 33 | 91% (73%-100%) | 140380 | 16655 | 1 |
| trailkeep@capture (control) | claude-sonnet-5-5 | 1 | 3 | 100% (100%-100%) | 104994 | 16424 | - |

Paired difference in pass rate vs `none` (same trap and seed, non-control traps):

| Arm | Model | Pairs | Difference (95% CI) |
|---|---|---|---|
| basic-memory | claude-sonnet-5-5 | 29 | +0% (+0% to +0%) |
| claude-mem | claude-sonnet-5-5 | 28 | +36% (+10% to +64%) |
| handoff | claude-sonnet-5-5 | 35 | +49% (+25% to +73%) |
| hindsight | claude-sonnet-5-5 | 29 | +0% (+0% to +0%) |
| native | claude-sonnet-5-5 | 29 | +41% (+14% to +70%) |
| oracle-note | claude-sonnet-5-5 | 72 | +71% (+54% to +86%) |
| resume | claude-sonnet-5-5 | 28 | +61% (+31% to +88%) |
| trailkeep | claude-sonnet-5-5 | 9 | +22% (+0% to +56%) |
| trailkeep@capture | claude-sonnet-5-5 | 33 | +88% (+70% to +100%) |
