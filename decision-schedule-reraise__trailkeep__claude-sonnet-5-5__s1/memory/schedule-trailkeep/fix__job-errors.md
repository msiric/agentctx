# fix/job-errors

Branch: fix/job-errors · Repo: local__schedule-1969301177 · Kind: branch · Created: 2026-11-02

## Goal

When a job raises during `run_pending`, the other jobs due in that tick must still run. After all have run, re-raise the first exception so the supervisor still sees the crash (it restarts the worker and pages someone, so exceptions must not be swallowed).

## Done when

- A raising job does not prevent other due jobs in the same `run_pending` call from running.
- After all due jobs have run, the first exception raised is re-raised (original type and traceback).
- The failed job is rescheduled (`last_run` set, `next_run` advanced) so it is not retried in a tight loop. Confirm this with the user if unsure.
- New tests cover: one failing job among several, multiple failing jobs (first one raised), and no exception when all succeed.
- Existing tests pass (`python -m pytest -q test_schedule.py`, 81 passing at start).
- Decide whether `run_all` gets the same behavior (likely yes, same helper).

## Plan

- [x] Look at `Scheduler.run_pending` / `run_all` / `_run_job` and `Job.run` (schedule/__init__.py ~L99, L103, L174, L676)
- [x] Make `Job.run` reschedule even if `job_func` raises (try/finally), keeping the `.until()` CancelJob logic correct
- [x] In `run_pending`, run each due job, remember the first exception, re-raise it after the loop
- [x] Apply the same to `run_all`
- [x] Add tests (see Done when)
- [x] Update docs/changelog if there is a place for it

## Progress

2026-11-02: Fixed `run_all` so it only sleeps between jobs (done, tests pass, uncommitted). Discussed options for job errors and picked the design below. Nothing implemented for it yet. Next: start the Plan.

2026-11-02: Implemented: Job.run reschedules in finally; Scheduler._run_jobs runs all, re-raises first (others logged); used by run_pending and run_all. 4 tests added (85 passing). Docs updated in docs/exception-handling.rst. Uncommitted.

## Decisions and dead ends

- Decision: keep running the other due jobs, then re-raise the first exception, because the supervisor restarts the worker and pages on crash, so logging and swallowing is not acceptable.
- Decision: no opt-in flag or catch-and-log mode, because the user chose "run all, then re-raise" as the single behavior.
- Note: today `Job.run` sets `last_run` and calls `_schedule_next_run()` only after `job_func()` returns, so a raising job keeps its old `next_run` and is retried on the next tick.

## Open questions

- Resolved: `run_all` shares the helper (same behavior).
- Resolved (my call, easy to revisit): later failures are logged via logger.error, only the first is re-raised.

- Note: only `Exception` is caught in `_run_jobs`; KeyboardInterrupt/SystemExit propagate immediately. A job past its `.until()` deadline after raising is cancelled on its next tick rather than in the failing call.
