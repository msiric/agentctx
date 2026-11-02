# Pilot (stage 1), 2026-11-02

- **Plan:** `plans/pilot.json`, 3 dev traps × `none`, `handoff`, `trailkeep`,
  `oracle-note` × 3 seeds.
- **Setup:** Claude Code 2.1.316 with claude-sonnet-5-5, on GitHub Actions.
- **Completion:** 36 of 36 episodes, with no harness errors and no usage
  limit reached.
- **Raw results:** on the `bench-results` branch.

| Trap | none | handoff | trailkeep | oracle-note | Gate |
|---|---|---|---|---|---|
| deadend-tinydb-streaming-write | 3/3 | 3/3 | 3/3 | 3/3 | **fails**: no headroom |
| constraint-dotenv-no-values | 3/3 | 3/3 | 3/3 | 3/3 | **fails**: no headroom |
| decision-schedule-reraise | 0/3 | 3/3 | 3/3 | 3/3 | passes |

Per the pre-registration, this pilot is not evidence for or against any
hypothesis. It checks the harness, the traps and the cost.

## What it established

- **The harness works end to end.** That covers isolated homes, real
  multi-turn sessions, the hidden checks, tokens and snapshots.
- **Two of three traps had no headroom.** On both, the model behaved
  correctly without memory: it kept the existing safe write path, and it
  didn't print secret values. A fact that matches good practice isn't a
  memory test for a model this strong. Traps need facts that are
  team-specific and arbitrary, or that go *against* the default good
  practice.
- **Outcomes were identical across all 3 seeds** in every trap × arm cell.
  Variance sits between traps, not between seeds, so more traps beat more
  seeds.
- **Cost:** about 2 minutes and $0.30–0.55 notional per episode, roughly $15
  notional for the pilot, on the subscription.

## How the one discriminating trap played out

- **`none`:** the plan only existed in the agent's last chat message. The
  next session found nothing in the repo and asked the user which option
  they wanted, so the task wasn't done. 0/3.
- **`trailkeep`:** when the user said "we'll build it next time", the agent
  invoked the effort skill and wrote the decision with its reason. The next
  session received it at start and built it. The log harvested 8 entries.
  3/3.
- **`handoff`:** the instruction alone worked just as well. 3/3.

## Capture is trailkeep's weak point

In the live smoke run of the dead-end trap, the "no effort file" hint fired
in both sessions and the agent ignored it both times. Nothing was captured.
Capture happened only when the user signalled that work would continue
("next time"). That's the first improvement hypothesis for the dev phase.
Next step: the headroom gate on the remaining 11 traps.
