# fix/job-errors

Branch: fix/job-errors · Repo: local__schedule-3395159457 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: Decision for job-error handling: in run_pending, keep running the other due jobs when one raises, then re-raise the FIRST exception after all have run. Reason: the user's supervisor restarts the worker and pages someone on crash, so errors must not be logged-and-swallowed. Rejected: log-only (option 2). Open/unconfirmed: whether to reschedule failed jobs via try/finally in Job.run (currently a raising job keeps its old next_run and retries every tick; I leaned toward rescheduling), and whether run_all gets the same handling. Not built yet; build next session. Also done this session: run_all(delay_seconds) no longer sleeps after the last job (no test added).
- 2026-11-04: Built run_pending error handling: runs all due jobs, logs each exception, re-raises FIRST after all ran (test RunPendingErrorTest in test_schedule.py). Still open/unconfirmed: try/finally reschedule in Job.run, and same handling for run_all. Not done pending user's call.

