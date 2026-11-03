# fix/job-errors

Branch: fix/job-errors · Repo: local__schedule-3040306465 · Kind: branch · Created: 2026-11-03

## Decisions and dead ends

- 2026-11-03: run_pending/run_all error handling: keep running the other due jobs, then re-raise the FIRST exception after all have run. Reason: supervisor restarts the worker and pages someone on crash, so exceptions must not be swallowed/only logged. Not yet built (planned for next session). Open: Job.run doesn't reschedule on failure (last_run/_schedule_next_run skipped), so a failing job retries every tick; consider try/finally.
- 2026-11-03: Built run_pending/run_all: run all due jobs, log each failure, re-raise FIRST exception afterwards (Scheduler in schedule/__init__.py). Job.run reschedule-on-failure still open.

