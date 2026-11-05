# fix/job-errors

Branch: fix/job-errors · Repo: local__schedule-904664273 · Kind: branch · Created: 2026-11-05

## Decisions and dead ends

- 2026-11-05: Decision (user's): run_pending must keep running the other due jobs when one raises, then re-raise the FIRST exception after all have run. Reason: their supervisor restarts the worker and pages someone on crash, so errors must not be logged-and-swallowed (no catch_exceptions=True style default). Not yet decided: whether a failed job reschedules normally (Job.run skips last_run/_schedule_next_run when job_func raises, so it currently retries every tick) - ask the user. Also apply to run_all? unconfirmed. Build is next session; nothing implemented yet. (Already done: run_all delay_seconds only sleeps between jobs.)
- 2026-11-05: Implemented run_pending per user's decision (run all due jobs, log each failure, re-raise FIRST exception after all ran) + test test_run_pending_runs_all_then_raises_first_error. Catches Exception only (my choice; KeyboardInterrupt/SystemExit still propagate immediately). Still open, ask user: (1) should a failed job reschedule normally or keep retrying every tick (currently retries every tick); (2) apply same behavior to run_all?

