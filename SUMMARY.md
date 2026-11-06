| Arm | Model | Traps | Runs | Pass rate (95% CI) | Last-session input tokens (median) | First request tokens (median) | Tool calls before first edit (median) |
|---|---|---|---|---|---|---|---|
| basic-memory | claude-sonnet-5-5 | 17 | 51 | 4% (0%-10%) | 135885 | 19194 | 1 |
| basic-memory (control) | claude-sonnet-5-5 | 2 | 6 | 100% (100%-100%) | 182778 | 19224 | - |
| claude-mem | claude-sonnet-5-5 | 17 | 51 | 35% (16%-57%) | 171434 | 21671 | 4 |
| claude-mem (control) | claude-sonnet-5-5 | 2 | 6 | 100% (100%-100%) | 174024 | 19392 | - |
| filler | claude-sonnet-5-5 | 6 | 18 | 6% (0%-17%) | 142631 | 17463 | 4 |
| filler (control) | claude-sonnet-5-5 | 1 | 3 | 100% (100%-100%) | 224794 | 17504 | - |
| handoff | claude-sonnet-5-5 | 42 | 126 | 72% (60%-84%) | 137744 | 16136 | 3 |
| handoff (control) | claude-sonnet-5-5 | 2 | 6 | 100% (100%-100%) | 162911 | 16186 | - |
| hindsight | claude-sonnet-5-5 | 17 | 51 | 2% (0%-6%) | 150006 | 18735 | 4 |
| hindsight (control) | claude-sonnet-5-5 | 2 | 6 | 100% (100%-100%) | 167074 | 18470 | - |
| hindsight@modelfix | claude-sonnet-5-5 | 1 | 1 | 100% (100%-100%) | 181128 | 19569 | - |
| native | claude-sonnet-5-5 | 17 | 51 | 33% (14%-55%) | 125773 | 16660 | 3 |
| native (control) | claude-sonnet-5-5 | 2 | 6 | 100% (100%-100%) | 152757 | 16675 | - |
| none | claude-sonnet-5-5 | 60 | 180 | 16% (8%-25%) | 118618 | 15925 | 2 |
| none (control) | claude-sonnet-5-5 | 2 | 6 | 100% (100%-100%) | 137914 | 15972 | - |
| none@rerun | claude-sonnet-5-5 | 23 | 69 | 3% (0%-9%) | 115498 | 15900 | 3 |
| oracle-note | claude-sonnet-5-5 | 60 | 180 | 98% (96%-100%) | 127338 | 16146 | 2 |
| oracle-note (control) | claude-sonnet-5-5 | 2 | 6 | 100% (100%-100%) | 149644 | 16116 | - |
| resume | claude-sonnet-5-5 | 17 | 51 | 75% (55%-92%) | 160004 | 22515 | 2 |
| resume (control) | claude-sonnet-5-5 | 2 | 6 | 100% (100%-100%) | 139246 | 15971 | - |
| trailkeep | claude-sonnet-5-5 | 38 | 96 | 78% (68%-87%) | 129880 | 16640 | 2 |
| trailkeep (control) | claude-sonnet-5-5 | 1 | 3 | 100% (100%-100%) | 201954 | 16399 | - |
| trailkeep@capture | claude-sonnet-5-5 | 11 | 33 | 91% (73%-100%) | 140380 | 16655 | 1 |
| trailkeep@capture (control) | claude-sonnet-5-5 | 1 | 3 | 100% (100%-100%) | 104994 | 16424 | - |
| trailkeep@finish | claude-sonnet-5-5 | 22 | 66 | 91% (82%-98%) | 139241 | 16771 | 3 |
| trailkeep@finish (control) | claude-sonnet-5-5 | 1 | 3 | 100% (100%-100%) | 122838 | 16472 | - |
| trailkeep@scope | claude-sonnet-5-5 | 11 | 33 | 94% (85%-100%) | 127794 | 16667 | 2 |
| trailkeep@scope (control) | claude-sonnet-5-5 | 1 | 3 | 100% (100%-100%) | 106535 | 16448 | - |
| trailkeep@wording | claude-sonnet-5-5 | 34 | 68 | 99% (96%-100%) | 140182 | 16876 | 2 |
| trailkeep@wording (control) | claude-sonnet-5-5 | 1 | 2 | 100% (100%-100%) | 149530 | 16516 | - |

Paired difference in pass rate vs `none` (same trap and seed, non-control traps):

| Arm | Model | Pairs | Difference (95% CI) |
|---|---|---|---|
| basic-memory | claude-sonnet-5-5 | 51 | -2% (-6% to +0%) |
| claude-mem | claude-sonnet-5-5 | 51 | +29% (+8% to +53%) |
| filler | claude-sonnet-5-5 | 18 | -6% (-17% to +0%) |
| handoff | claude-sonnet-5-5 | 126 | +63% (+50% to +76%) |
| hindsight | claude-sonnet-5-5 | 51 | -4% (-12% to +0%) |
| hindsight@modelfix | claude-sonnet-5-5 | 1 | +100% (+100% to +100%) |
| native | claude-sonnet-5-5 | 51 | +27% (+8% to +49%) |
| none@rerun | claude-sonnet-5-5 | 69 | +0% (-4% to +4%) |
| oracle-note | claude-sonnet-5-5 | 180 | +82% (+73% to +91%) |
| resume | claude-sonnet-5-5 | 51 | +69% (+47% to +88%) |
| trailkeep | claude-sonnet-5-5 | 96 | +74% (+64% to +83%) |
| trailkeep@capture | claude-sonnet-5-5 | 33 | +88% (+70% to +100%) |
| trailkeep@finish | claude-sonnet-5-5 | 66 | +88% (+79% to +95%) |
| trailkeep@scope | claude-sonnet-5-5 | 33 | +91% (+82% to +100%) |
| trailkeep@wording | claude-sonnet-5-5 | 68 | +94% (+88% to +99%) |
