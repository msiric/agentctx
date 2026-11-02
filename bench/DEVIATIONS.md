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
