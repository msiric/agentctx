# HANDOFF

## State
Added `Scheduler.get_jobs_for(func)` (schedule/__init__.py), tests in test_schedule.py
(`test_get_jobs_for`). Committed on feature/jobs-by-func.

## Decisions
- Matches on `job.job_func.func == func`: `do()` wraps the function in a `functools.partial`,
  so comparing against `job_func` itself would never match.
- Bound args/kwargs are ignored; all jobs scheduled with `func` are returned.
- Returns a new list, like `get_jobs`, so cancelling while iterating is safe.
- Jobs with `job_func is None` are skipped defensively.

- No module-level `schedule.get_jobs_for` shortcut: project is moving off the global default
  scheduler, so new APIs go on `Scheduler` only. (Initially added, then removed on request.)
  docs/reference.rst already renders Scheduler members via autoclass.

## Failed approaches
None.

---

# Task: pause/resume by tag (branch feature/pause-jobs, uncommitted)

## State
`Scheduler.pause(tag)` / `Scheduler.resume(tag)` added in schedule/__init__.py; `run_pending`
skips jobs whose tags intersect `Scheduler._paused_tags`. Tests: `test_pause_and_resume_by_tag`,
`test_pause_does_not_affect_run_all` in test_schedule.py. Full suite passes (84).

## Decisions
- State is a set of paused *tags* on the scheduler, not a flag per job: jobs tagged after
  `pause()` are also paused, and a job with several tags is paused if any of them is.
- `next_run` is not touched while paused. A job that came due runs once on the first
  `run_pending()` after resume (consistent with run_pending's "no replay of missed runs").
- `run_all` deliberately ignores pausing (it means "run regardless of schedule").
- `clear(tag)` does not unpause the tag.
- Scheduler-only, no module-level `schedule.pause` shortcut (same rule as get_jobs_for above).
  Say so if you want shortcuts.

## Failed approaches
None.
