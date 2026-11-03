| Arm | Model | Traps | Runs | Pass rate (95% CI) | Last-session input tokens (median) | First request tokens (median) | Tool calls before first edit (median) |
|---|---|---|---|---|---|---|---|
| basic-memory | claude-sonnet-5-5 | 17 | 42 | 5% (0%-12%) | 134438 | 19193 | 1 |
| basic-memory (control) | claude-sonnet-5-5 | 2 | 4 | 100% (100%-100%) | 147937 | 19224 | - |
| claude-mem | claude-sonnet-5-5 | 17 | 42 | 38% (18%-59%) | 176428 | 21642 | 4 |
| claude-mem (control) | claude-sonnet-5-5 | 2 | 4 | 100% (100%-100%) | 143127 | 19402 | - |
| handoff | claude-sonnet-5-5 | 19 | 47 | 64% (42%-84%) | 134442 | 16141 | 2 |
| handoff (control) | claude-sonnet-5-5 | 2 | 4 | 100% (100%-100%) | 127972 | 16196 | - |
| hindsight | claude-sonnet-5-5 | 17 | 42 | 2% (0%-8%) | 150790 | 18704 | 4 |
| hindsight (control) | claude-sonnet-5-5 | 2 | 4 | 100% (100%-100%) | 151280 | 18423 | - |
| native | claude-sonnet-5-5 | 17 | 42 | 36% (13%-60%) | 125756 | 16662 | 3 |
| native (control) | claude-sonnet-5-5 | 2 | 4 | 100% (100%-100%) | 115457 | 16683 | - |
| none | claude-sonnet-5-5 | 24 | 63 | 32% (14%-51%) | 120287 | 15928 | 3 |
| none (control) | claude-sonnet-5-5 | 2 | 4 | 100% (100%-100%) | 120060 | 15984 | - |
| oracle-note | claude-sonnet-5-5 | 24 | 63 | 97% (90%-100%) | 122356 | 16142 | 2 |
| oracle-note (control) | claude-sonnet-5-5 | 2 | 4 | 100% (100%-100%) | 134710 | 16126 | - |
| resume | claude-sonnet-5-5 | 17 | 42 | 74% (54%-91%) | 158142 | 22518 | 1 |
| resume (control) | claude-sonnet-5-5 | 2 | 4 | 100% (100%-100%) | 123554 | 15982 | - |
| trailkeep | claude-sonnet-5-5 | 15 | 18 | 61% (33%-84%) | 126560 | 16500 | 2 |
| trailkeep (control) | claude-sonnet-5-5 | 1 | 1 | 100% (100%-100%) | 201954 | 16402 | - |
| trailkeep@capture | claude-sonnet-5-5 | 11 | 33 | 91% (73%-100%) | 140380 | 16655 | 1 |
| trailkeep@capture (control) | claude-sonnet-5-5 | 1 | 3 | 100% (100%-100%) | 104994 | 16424 | - |

Paired difference in pass rate vs `none` (same trap and seed, non-control traps):

| Arm | Model | Pairs | Difference (95% CI) |
|---|---|---|---|
| basic-memory | claude-sonnet-5-5 | 42 | -2% (-8% to +0%) |
| claude-mem | claude-sonnet-5-5 | 42 | +31% (+7% to +55%) |
| handoff | claude-sonnet-5-5 | 47 | +47% (+24% to +69%) |
| hindsight | claude-sonnet-5-5 | 42 | -5% (-15% to +0%) |
| native | claude-sonnet-5-5 | 42 | +29% (+2% to +54%) |
| oracle-note | claude-sonnet-5-5 | 63 | +65% (+46% to +83%) |
| resume | claude-sonnet-5-5 | 42 | +67% (+43% to +88%) |
| trailkeep | claude-sonnet-5-5 | 18 | +50% (+24% to +75%) |
| trailkeep@capture | claude-sonnet-5-5 | 33 | +88% (+70% to +100%) |
