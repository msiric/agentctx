# Stage 0: context added at session start (no model calls)

Measured with `tools/injection-cost`. Claude Code ran one turn against
`tools/mock-anthropic.py`, and we measured the text of the first request it
sent. Each figure is characters added relative to `none` at the same history
length. Tokens are roughly characters ÷ 4. Raw data:
`injection-cost.json`.

| Sessions of stored history | `native` (auto memory) | `handoff` | `trailkeep` |
|---:|---:|---:|---:|
| 0 | 12,835 (~3.2k tok) | 636 | 995 (~250 tok) |
| 1 | 13,582 | 642 | 1,910 |
| 5 | 14,974 | 642 | 3,358 |
| 10 | 16,705 | 642 | 5,162 |
| 20 | 20,215 | 642 | 8,822 (~2.2k tok) |
| 40 | 27,235 | 642 | 1,329 (pointer only) |

"History" is simulated: each earlier session adds one progress line and two
decision lines of realistic length (see the script).

## Caveats

- **`native`:** its growth here comes from a synthetic MEMORY.md holding the
  same lines. Real auto memory keeps a short index and reads topic files on
  demand. Only its empty-state cost (row 0) is a direct measurement of
  shipped behaviour.
- **`handoff`:** the instruction is injected, but HANDOFF.md isn't; the agent
  reads it with a tool call later. Reading it costs tokens that this table
  doesn't count. The live runs' last-session input tokens do count them.

## Findings

1. **Built-in auto memory costs about 3.2k tokens in every session before it
   has stored anything.** That's its instructions to the model. It's about
   13× trailkeep's empty-state cost.
2. **trailkeep's empty-state cost is about 250 tokens, not the 60 the README
   claimed.** On a feature branch with no effort file, in Claude Code, it
   breaks down as:
   - about 300 characters for the skill description
   - about 450 characters of Claude Code's standard wrapper, which shows up
     because install creates a near-empty global instructions file
   - about 200 characters for the "no effort file" hint
3. **trailkeep's injection hits a cliff.** The effort file is injected whole
   until it passes the 9,000-character budget (about 20 sessions of unfolded
   notes here). From then on the injection is only a pointer, and reading the
   file is left to the agent. The skill tells agents to fold old progress
   lines, but if they don't, retention could drop sharply at that point.
   Candidate fix, to test on dev traps: inject the goal, open plan items,
   latest progress and decisions, and point to the rest.
