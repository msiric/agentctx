# HANDOFF

## State
- `Scheduler.run_all(delay_seconds)` now sleeps only between jobs, not after the last (schedule/__init__.py). Test added in test_schedule.py.

## Decisions
- Iterate over a snapshot (`self.jobs[:]`) with an index: jobs may cancel themselves during the run, so the snapshot length is the right "last job" check.

## Failed approaches
- None.

## Job exceptions in run_pending / run_all (implemented, uncommitted)
- `Scheduler._run_job_collecting` catches `Exception` per job (logs with traceback, appends to a list); `_raise_first` re-raises the first after all jobs ran and logs a count if more than one failed. Used by both `run_pending` and `run_all` (schedule/__init__.py). `run_all` still sleeps between jobs.
- Catches `Exception` only, so KeyboardInterrupt/SystemExit still abort immediately.
- Decision (user): run all other due jobs, then re-raise the FIRST exception; no ExceptionGroup (needs 3.11+). Rejected: log-and-swallow (supervisor must see the crash), opt-in flag/hook.
- Tests added in test_schedule.py (run_pending and run_all). Suite: 43 passed, 41 skipped.
- Test gotcha: jobs must be created inside `mock_datetime` for run_pending to see them as due, since failed jobs are never rescheduled.

## Open (ask user before changing)
- `Job.run` calls `job_func()` before setting `last_run`/`_schedule_next_run()`, so a failing job is never rescheduled and retries on every tick. Whether to reschedule in a `finally` is undecided; changes retry semantics, so not touched.
