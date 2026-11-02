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
seeded by the commit hash that adds the traps. Nobody picks.
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
