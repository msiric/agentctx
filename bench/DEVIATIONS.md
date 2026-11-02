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
