# HANDOFF

## State
Added `Scheduler.get_jobs_for(func)`
(schedule/__init__.py), returning all jobs whose scheduled function is `func`.
Test: `test_get_jobs_for` in test_schedule.py.

## Decisions
- Match on `job.job_func.func == func`: `Job.do` wraps the callable in a
  `functools.partial`, so the original function is `.func`. Matching ignores args,
  so `do(foo, 1)` and `do(foo, 2)` are both returned.
- `job_func is None` guarded (jobs in `scheduler.jobs` normally always have one).
- Returns a new list, so callers can safely cancel while iterating.

## Pause/resume
`Scheduler.pause(tag)` / `resume(tag)` set `Job.paused` (schedule/__init__.py);
`run_pending` skips paused jobs. Tests: `test_pause_resume`, `test_pause_unknown_tag`.
- `run_all` still runs paused jobs (explicit "run everything"); say so if that should change.
- `next_run` is not recomputed on resume, so a job that came due while paused
  runs on the next `run_pending`. Alternative: reschedule on resume.
- Scheduler-only, no module-level shortcut (same reason as below).
- Test gotcha: jobs must be created inside `mock_datetime`, else next_run is
  real-now and the mocked past clock never makes them due.

## Not done
- No docs/HISTORY entry added.

## Decision: no module-level shortcut
Deliberately NOT added as `schedule.get_jobs_for`: the project is moving off the
global default scheduler, so new APIs go on `Scheduler` only. An earlier draft had
the shortcut; it was removed at the user's request.
