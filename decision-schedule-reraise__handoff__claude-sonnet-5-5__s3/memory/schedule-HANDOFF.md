# Handoff

## Current state
- Branch `fix/job-errors`. Nothing committed.
- Done (uncommitted): `Scheduler.run_all(delay_seconds=...)` in `schedule/__init__.py` now
  sleeps only between jobs, not after the last one. Tests pass (40 passed, 41 skipped).
- Done (uncommitted): `run_pending` and `run_all` now run every due job even if one raises, then
  re-raise the first exception (others logged) via `_run_job_collecting` / `_raise_first` in
  `Scheduler`. Test `TestJobException` added in `test_schedule.py`. 41 passed, 41 skipped.
- Still open: rescheduling a failed job (see below). NOT done; failed job still retries every tick.
- Only `Exception` is collected; KeyboardInterrupt/SystemExit propagate immediately (deliberate).

## Next task: job exceptions in run_pending
Problem: `Job.run()` calls `job_func()` before setting `last_run` / `_schedule_next_run()`
(`schedule/__init__.py` ~line 693). If it raises, the exception escapes `run_pending`, the
remaining due jobs in that tick never run, and the failed job is not rescheduled (its
`next_run` stays in the past, so it retries on the very next tick). `run_all` has the same issue.

Decision: run all the other due jobs, then re-raise the first exception once they've all run.
Reason: the user's supervisor restarts the worker and pages someone on a crash, so errors must
not be swallowed or only logged.

Plan:
- Collect exceptions per job in `run_pending` (and `run_all`), keep going, re-raise the first
  one at the end. Log any further ones (`ExceptionGroup` is 3.11+; the library supports older).
- Open question to confirm with the user: reschedule a failed job normally (e.g.
  `_schedule_next_run()` in a `finally` in `Job.run`) instead of retrying every tick? I lean
  yes, matching the "missed jobs run once" philosophy in the `run_pending` docstring. Also
  decide whether `last_run` is updated on failure.
- Add tests: other due jobs still run, first exception is re-raised, failed job rescheduled.

## Decisions
- `run_all` iterates a snapshot (`jobs = self.jobs[:]`) with `enumerate` and skips the sleep
  on the last index, so jobs that cancel themselves mid-run don't affect iteration.
- Options rejected for the exception work: log-and-swallow (hides failures from the
  supervisor); opt-in `on_error` hook (leaves the bug as the default).

## Failed approaches
- First draft of the test used `unittest.TestCase` (not imported; file uses pytest-style classes) and
  a class name not starting with `Test`, so pytest silently didn't collect it. Fixed.

## Open
- No test yet asserting `time.sleep` is not called after the last job in `run_all`.
