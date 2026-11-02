# Benchmark

Does trailkeep help an agent's next session respect what earlier sessions
learned, and at what context cost? It is compared with no memory, the
agents' built-in memory, a plain handoff file and other memory tools.

- `PREREGISTRATION.md`: hypotheses, arms, metrics and analysis, fixed before any live run
- `TRAP-SPEC.md`: what a test case (trap) is
- `ARMS.md`: exactly how each condition is set up
- `traps/`: the test cases
- `plans/`: which traps × arms × seeds a run covers
- `harness/episode.py`: runs one trap under one arm (all sessions, then the hidden check)
- `harness/matrix.py`: runs a plan resumably within a time budget; pauses at usage limits
- `harness/summarize.py`: pass rates with bootstrap intervals, paired differences, token medians
- `tools/mock-anthropic.py`: a fake Messages API for model-free tests of the harness
- `tools/injection-cost`: stage 0, what each arm adds to the request at session start
- `tools/validate-trap`: checks a trap's oracle against its reference patches

Live runs happen in CI (`.github/workflows/bench.yml`) on the
`CLAUDE_CODE_OAUTH_TOKEN` secret. Results land on the `bench-results` branch.
