# Pre-registration: trailkeep cross-session benchmark

Committed before any live run. Any change after the first live run goes in
`DEVIATIONS.md`, with the date and the reason, and stays visible in git
history. Every run gets reported, including runs where trailkeep loses or
shows no difference.

## Question

When a coding task spans several agent sessions, does trailkeep help the next
session respect what earlier sessions learned, and at what context cost?
How does it compare with:
- doing nothing
- the agents' built-in memory
- a plain handoff file
- other memory tools

## Hypotheses

Primary. Tested on non-control traps, held-out set, Claude Code with the
main model:

- **H1:** trailkeep has a higher last-session pass rate than no memory.
- **H2a:** trailkeep has a higher pass rate than the agent's built-in memory.
- **H2b:** trailkeep has a higher pass rate than the HANDOFF.md instruction.

Secondary. Estimated with confidence intervals, no significance claim:

- **H3, lean:** trailkeep's median injection at session start stays under
  2,500 tokens. Its last-session input tokens are no higher than no memory's
  (less rediscovery should offset the injection).
- **H4, no harm:** on control traps, trailkeep's pass rate is within 10
  points of no memory's.
- **H5, hygiene:** on superseded traps, trailkeep's rate of using the stale
  fact is below no memory's and below built-in memory's.
- **H6, cross-agent:** with Claude Code for the earlier sessions and Codex
  for the last, trailkeep's pass rate is no lower than with Claude Code
  throughout. This is exploratory and depends on Codex access.

Anything else is labelled exploratory when reported.

## Traps

- Format and validity rules are in `TRAP-SPEC.md`.
- Traps are written by an agent given only that spec and a neutral
  description of the benchmark. It is never shown trailkeep or told which
  tools are compared.
- Traps are not edited to suit any condition. A trap may be fixed only when
  it is broken, meaning it fails `tools/validate-trap` or has a bug in its
  check. Every fix is logged in `DEVIATIONS.md`.

**Dev and held-out split.** After authoring, `tools/split-traps` assigns
about a third of the traps to held-out. The assignment is deterministic and
seeded by the commit hash that adds the traps. The same tool also picks the 3 pilot traps from the dev set. Nobody picks. The result is in `plans/SPLIT.json`.
- trailkeep changes may be informed by dev results only.
- Held-out traps run once, against frozen versions of every tool, with
  versions recorded. Held-out results are the ones quoted as findings.

**Headroom gate.** A trap is dropped from the analysis if, in the pilot, no
memory passes it in at least 2 of 3 seeds (no headroom), or the perfect note
fails it in at least 2 of 3 seeds (broken). The rule looks only at those two
arms, never at trailkeep or competitor results.

## Arms

Every arm gets the same:
- traps
- user turns, including the fixed closing message
- model
- turn budget
- fresh home directory

Each tool is installed following its own README at a pinned version, with
the defaults that README recommends. Exact setup is in `ARMS.md`, frozen
before the pilot.

**Built-in memory.** It is switched off in every arm except `native`, so
each tool is measured on its own. One exploratory arm,
`trailkeep+native`, keeps it on, which is what a real trailkeep user gets.

| Arm | Description |
|---|---|
| `none` | No memory. Built-in memory switched off. The repo and its git history are all there is. |
| `native` | The agent's built-in memory, as shipped: Claude Code auto memory; Codex memories where available. |
| `handoff` | One instruction in the user's global agent instructions file: keep `HANDOFF.md` at the repo root with state, decisions and dead ends, and read it at the start. |
| `trailkeep` | `trailkeep install`, defaults. |
| `claude-mem` | claude-mem plugin (Claude Code only). |
| `basic-memory` | Basic Memory MCP server with its recommended instructions. |
| `hindsight` | Hindsight, with its recommended hook setup. |
| `filler` | No memory, plus irrelevant text injected at session start, matched in length to trailkeep's mean injection on that trap. Separates "the content helps" from "more context helps or hurts". |
| `oracle-note` | A perfect handoff note listing the trap's facts, injected at the last session's start. Retention ceiling. |
| `resume` | The last session resumes the previous session's full transcript. Ceiling for retention, and shows what not being lean costs. |

## Protocol

- Each session is a separate agent process with multiple turns. The user
  turns come from `trap.json` and are sent one at a time. Each session ends
  with the fixed closing message "That's all for today, thanks."
- Agents run with permission prompts bypassed inside an isolated container.
  Each session is limited to `budget.max_turns_per_session` turns and 20
  minutes.
- `oracle/` and `reference/` never enter the agent's filesystem.
- Across arms, run order is randomized per seed so model drift lands evenly.
- Recorded per run:
  - CLI versions, model IDs and tool versions
  - the trailkeep commit
  - full transcripts and token usage per session

## Outcomes

**Primary:** last-session pass, the exit status of `oracle/check.sh`.

**Secondary:**
- Per-fact retention, from the check's per-fact lines.
- Rates of using a superseded fact, retrying a dead end, and applying a fact
  outside its scope. Stale use is scored by the check. Retried dead ends and
  scope errors come from transcripts, classified by a judge that sees
  neither the arm name nor the tool's files.
- Tokens injected at session start. Cumulative input, cached input and
  output tokens per session.
- Tool calls before the first edit in the last session, as a measure of
  rediscovery.
- Wall time, and subscription usage where reported.
- User actions each arm requires. This is a property of the arm, reported
  alongside the results.

**Failure taxonomy.** Every trailkeep failure gets exactly one label,
assigned blind to arm from the transcript and the tool's stored files:
- **Capture miss:** the fact never got written down.
- **Retrieval miss:** it was written down but not injected or found.
- **Use failure:** it was injected but ignored.
- **Pollution:** a stale or irrelevant stored fact caused the failure.
- **Other.**

## Analysis

- **Pairing:** by trap × seed. The effect is the difference in pass rate,
  trailkeep minus the comparator.
- **Confidence intervals:** 95%, from a cluster bootstrap over traps with
  10,000 resamples.
- **Tests:** a one-sided paired permutation test for each of H1, H2a and
  H2b, with Holm correction across the three at α = 0.05. A non-significant
  result is reported as such, never as equivalence.
- **Sizing:** after the pilot, seeds per cell are set so that the expected
  95% interval for H1 is no wider than ±15 points. If usage limits force a
  cut, seeds are reduced before traps or arms.
- **Charts:** pass rate against median injected tokens, one point per arm,
  with CIs.

## Stages

0. Model-free tests: injected size under simulated growth, and output size
   of `log` queries.
1. **Pilot:** 3 dev traps × `none`, `handoff`, `trailkeep`, `oracle-note` ×
   3 seeds, Claude Code with the main model. It checks:
   - that the harness runs end to end
   - the headroom gate
   - variance
   - usage per episode
2. **Dev matrix:** all arms on the dev traps. Failure taxonomy, then
   trailkeep changes, then a re-run.
3. **Held-out run:** once, on frozen versions. Findings are quoted from this
   stage.

## Addendum: held-out set 2 (committed 2026-11-04, before its traps exist)

Held-out set 1 left H2b (trailkeep vs the handoff file) unresolved: +22
points, p = 0.11 on 6 traps. Set 1 is no longer unseen, since trailkeep 0.5.0
was designed after reading its failures. Set 2 is a fresh test.

**Traps.** 12 new traps, written by two new blind authors (6 Python, 6
TypeScript/JavaScript), 2 per fact family: decision, dead-end, constraint,
superseded, branch-isolation, cross-repo-preference. The authors get the same
spec, the same blindness, and the batch-2 brief with the gate lessons added.
They use repos that no earlier trap used. Every trap in set 2 is held-out;
there is no dev split, because trailkeep doesn't change between now and the
run.

**Gate.** Same rule as before: `none` and `oracle-note`, 3 seeds. Drop a trap
if `none` passes 2 or more of 3, or `oracle-note` fails 2 or more of 3.

**Run.** On the kept traps: `trailkeep` (0.5.0), `handoff` and `none`, 3
seeds, frozen versions (`PINS.env`), dispatched once from a frozen branch.
`none` runs again rather than reusing its gate cells, since the gate selected
traps on those cells.

**Primary.** Two one-sided tests on set 2 only, Holm-corrected at α = 0.05,
using the same method as before (exact sign-flip permutation over trap × seed
pairs; trap-level version reported as a sensitivity check):
- **H2b-2:** trailkeep has a higher pass rate than handoff.
- **H1-2:** trailkeep has a higher pass rate than no memory.

**Secondary.** Tokens added at session start, H5 on the superseded traps,
failure labels for every trailkeep and handoff failure. Pooling set 1 with
set 2 mixes trailkeep versions, so any pooled result is exploratory.

No trap is edited after the gate unless it is broken (logged in
`DEVIATIONS.md`). Set 2 runs once and is reported whatever it shows.

## Addendum: held-out set 3 (committed 2026-11-05, before its traps exist)

Set 2 tied trailkeep 0.5.0 with the handoff file (79% each, p = 0.62).
trailkeep 0.5.1 was changed after reading set 2's failures (the capture rule
now asks the agent to check before finishing that nothing is left
unrecorded), so set 2 is no longer unseen. Set 3 is a fresh test of 0.5.1.

**Traps.** 12 new traps from two new blind authors (6 Python, 6
TypeScript/JavaScript), 2 per fact family, same spec and blindness as set 2,
with set 2's gate lessons added to the brief. They use repos that no earlier
trap used. Every trap is held-out.

**Gate.** Same rule: `none` and `oracle-note`, 3 seeds. Drop a trap if `none`
passes 2 or more of 3, or `oracle-note` fails 2 or more of 3.

**Run.** On the kept traps: `trailkeep` (0.5.1), `handoff` and `none`, 3
seeds, frozen versions (`PINS.env`), dispatched from a frozen branch. `none`
runs under a fresh label (`none@rerun`) so the gate cells are not reused.

**Primary.** Same method as set 2, on set 3 only, Holm-corrected at α = 0.05:
- **H2b-3:** trailkeep has a higher pass rate than handoff.
- **H1-3:** trailkeep has a higher pass rate than no memory.

**Secondary.** Tokens added at session start, H5 on the superseded traps,
failure labels for every trailkeep and handoff failure. Any pooling with
earlier sets is exploratory.

No trap is edited after the gate unless it is broken (logged in
`DEVIATIONS.md`). Set 3 runs once and is reported whatever it shows.

## Addendum: held-out set 4 (committed 2026-11-06, before its traps exist)

Set 3 put trailkeep 0.5.1 11 points ahead of the handoff file, not
significant (p = 0.17). trailkeep 0.5.2 was changed after reading set 3's
failures (the capture rule now asks for notes worded as instructions, as
broad as the user's rule, with the agent's own choices marked). Set 3 is no
longer unseen. Set 4 is a fresh test of 0.5.2.

Same design as set 3: 12 new traps from two new blind authors (6 Python, 6
TypeScript/JavaScript), 2 per family, on repos no earlier trap used; the same
gate; `trailkeep` (0.5.2), `handoff` and `none@rerun`, 3 seeds, frozen
versions, dispatched from a frozen branch.

**Primary**, on set 4 only, Holm-corrected at α = 0.05, same method:
- **H2b-4:** trailkeep has a higher pass rate than handoff.
- **H1-4:** trailkeep has a higher pass rate than no memory.

Secondary and exploratory analyses as in set 3. No trap is edited after the
gate unless it is broken. Set 4 runs once and is reported whatever it shows.
