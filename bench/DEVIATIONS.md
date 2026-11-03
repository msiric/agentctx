# Deviations from the pre-registration

Each entry gives the date, what changed, and why. Every one was decided
before the results it could affect were seen.

## 2026-11-02: headroom gate run on every trap, not just the pilot's three

- **What changed:** The pre-registration applies the headroom gate "in the
  pilot", which covered 3 traps. The gate now also runs on the other 11
  traps, using only the `none` and `oracle-note` arms with 3 seeds each
  (`plans/gate.json`).
- **Why:** In the pilot, 2 of 3 traps failed the gate. No memory passed them
  3/3, because the model inferred the "fact" from good practice. The dev
  matrix shouldn't spend runs on traps that can't show a difference.
- **Why this is safe:** Neither arm involves trailkeep or a competitor, so
  the gate can't be tuned toward any tool. For held-out traps, these runs
  count as their `none` and `oracle-note` results; those arms don't depend
  on the trailkeep version.

## 2026-11-02: snapshot fix (harness, no effect on outcomes)

The `trailkeep` arm's snapshot left out effort files, because `.trailkeep`
ignores itself in git. The snapshot now deletes `.gitignore` files from its
copy. This affects only the files saved for the failure taxonomy, not any
run's outcome.

## 2026-11-02: second batch of 12 traps, with a revised authoring brief

- **What changed:** Two new blind authors are writing a second batch of 12
  traps. They have the same spec and the same blindness to which tools are
  compared. The brief now adds the pilot's lesson:
  - facts must be team-specific, or must go against default good practice
  - the last session's task must be concrete enough that a no-memory agent
    attempts it rather than stopping to ask
  - branch-isolation results must not depend on whether the agent commits
- **Why:** The pilot showed that facts which coincide with good practice
  give no headroom. The new guidance applies to every arm alike. Each new
  trap still has to pass `validate-trap` and the headroom gate.
- **Split:** `tools/split-traps` treats the second batch as its own group.
  Held-out traps are assigned by the hash of the commit that adds that
  batch, using the same rule as before. Batch-1 assignments stay as they
  are.

## 2026-11-02: the headroom gate doesn't apply to control traps

The gate rule as written would drop every control trap, since `none` is
supposed to pass those. Controls exist to measure overhead (H4), so they
aren't gated. This was decided when the batch-1 gate results came in, and it
was obvious from the controls' purpose. No other trap's outcome is affected.

## 2026-11-02: competitor arms fixed after their smoke run (setup only)

The smoke run (one episode each on `decision-schedule-reraise`) failed all
three competitors, and in each case the tool never ran as its README
intends. None of these episodes counts as a result.

- **claude-mem:** its hooks call a launcher in `~/.local/bin`, which wasn't on
  the agents' `PATH`, so every hook failed ("memory hooks are not active").
  The harness now puts `$HOME/.local/bin` first on `PATH` for **every** arm,
  as on a normal machine. This also affects trailkeep, which links its CLI
  there, so trailkeep results from before this change are not pooled with
  later ones (only the pilot had any).
- **Basic Memory:** `bm install claude-code` waits for a confirmation, so it
  installed nothing without a terminal. It now runs with `--yes` and the arm
  fails if the plugin is missing. `/basic-memory:bm-setup` is an interview;
  the scripted user now accepts every suggested default and confirms.
- **Hindsight:** Gemini's free tier allows 20 requests a day, which the first
  retention used up, so nothing from the session was stored. Hindsight now
  uses its `claude-code` LLM provider with the same subscription token as the
  sessions, the way claude-mem works. After each session the harness waits
  for Hindsight's queue to empty (up to 5 minutes) instead of a fixed 90 s.
- **claude-mem, second try:** its hooks now ran, but its worker reads the
  login from Claude Code's credential store (`~/.claude/.credentials.json`),
  not from `CLAUDE_CODE_OAUTH_TOKEN`, so every summary failed with "not
  logged in" and nothing was stored. The arm now writes that store from the
  same token, as a logged-in user has it, and deletes it after the episode.
  The results workflow now redacts any credential before saving files.
- **Basic Memory and Hindsight, second try:** both ran as intended (Basic
  Memory's setup completed with its proactive capture style on; Hindsight
  stored and recalled memories). Their smoke episodes stand as smoke checks
  only and are not part of any analysis.

## 2026-11-02: cells removed before the dev matrix

Before the dev matrix, the `bench-results` branch dropped the pilot's
`trailkeep` cells (run before the `PATH` change above) and the three
competitor smoke cells (smoke checks only). The dev matrix re-runs them under
the current harness. The pilot's `none`, `handoff` and `oracle-note` cells,
and the gate cells, are kept, since nothing these arms use changed.

## 2026-11-03: trailkeep v0.3.2 dropped from the rest of the dev matrix

After seed 1, trailkeep v0.3.2 passed 1 of 8 fact traps, and all 7 failures
were capture misses (`results/dev-notes.md`). Its remaining dev seeds were
dropped to save subscription usage; the cells already run are kept. The
changed version runs as `trailkeep@capture`. Dev results are exploratory
either way; the held-out run is unaffected.

## 2026-11-03: held-out run setup

- **trailkeep under test:** 0.4.0 (published to npm with provenance), the
  dev arm `trailkeep@capture` plus a version bump. In the held-out plan it is
  the arm `trailkeep`.
- **Frozen versions:** `bench/PINS.env`. claude-mem and the Basic Memory
  plugin install from checkouts at a fixed tag/commit instead of their
  default branches. During the dev matrix claude-mem moved from 15.8.3 to
  15.9.0 and Claude Code from 2.1.316 to 2.1.317; the held-out run uses the
  newer of each. claude-mem's launcher may still fetch from npm at first run;
  its version is recorded per cell.
- **Gate cells not reused:** the held-out traps' `none` and `oracle-note`
  cells from the headroom gate ran under an earlier Claude Code and harness.
  They move to `gate/` on the results branch and the held-out run re-runs
  both arms, so every held-out cell shares one set of versions.
- **Filler sizing:** the plan said filler matches "trailkeep's mean
  injection on that trap". trailkeep has no cells on held-out traps until
  this run, so filler runs as part 2 (`heldout-filler`), sized per trap from
  part 1's trailkeep cells (mean first-request tokens minus `none`'s, × 4
  characters). Nothing else in the plan changes.
