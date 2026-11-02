# HANDOFF

## Current state
- `Scheduler.run_all(delay_seconds)` in `schedule/__init__.py` now sleeps only between jobs, not after the last one.
- Iterates over a copy of `self.jobs` (as before), using the copy's length for the "last job" check, so jobs that cancel themselves don't skew it.
- Existing tests pass (40 passed, 41 skipped). No dedicated test for the delay yet.

## Decisions
- Used `enumerate` over the copied list rather than checking `self.jobs`, since jobs may be removed mid-run.

## Failed approaches
- None.

## Job exceptions starve other due jobs (implemented, uncommitted)
- `Scheduler.run_pending` and `run_all` catch `Exception` per job, log it, keep running the rest, then re-raise the **first** exception. Reason (user): supervisor restarts worker and pages on crash, so errors must not be swallowed.
- `Job.run` reschedules (`last_run`, `_schedule_next_run`) on exception before re-raising, to avoid hot retry every tick. Not explicitly confirmed with user.
- `run_all` got the same treatment for consistency (assumed, not confirmed). It still sleeps between jobs after a failure.
- Tests added in `JobErrorTests` (test_schedule.py). Suite: 42 passed, 41 skipped.
- Caveats: only `Exception` is caught (KeyboardInterrupt/SystemExit propagate immediately). Later exceptions are logged but not raised. A failed job with `.until()` past deadline is not cancelled on the exception path.
