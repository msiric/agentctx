# fix/job-errors

Branch: fix/job-errors · Repo: local__schedule-1089270487 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: Decision: run_pending should run all due jobs even if one raises, then re-raise the FIRST exception after all have run (not log-and-swallow). Reason: the user's supervisor restarts the worker and pages someone on crash, so errors must still propagate. Open points: failed job should still reschedule (Job.run updates last_run/next_run only after job_func succeeds, so a failing job stays due and sorts first every tick); decide whether run_all gets the same treatment; ExceptionGroup is 3.11+ only, so re-raise the first exception. Not built yet.
- 2026-11-04: run_pending now implemented: runs all due jobs, reschedules failed job in Scheduler.run_pending (not Job.run, to keep Job.run semantics unchanged), re-raises first exception. run_all NOT changed - still undecided.

