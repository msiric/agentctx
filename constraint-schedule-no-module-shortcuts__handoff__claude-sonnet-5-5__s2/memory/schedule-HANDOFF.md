# HANDOFF

## State
Branch feature/pause-jobs. Done (uncommitted): `Scheduler.pause(tag)` / `Scheduler.resume(tag)`,
`Job.paused` flag, `run_pending` skips paused jobs. Tests: `test_pause_resume_by_tag`,
`test_pause_unknown_tag_is_noop` in test_schedule.py. Full suite passes (84).
Earlier: `Scheduler.get_jobs_for(func)` (committed, 85ced73).

## Decisions
- Pause is a boolean on Job (`paused`), set via tag lookup; jobs stay in scheduler.jobs.
- `tag` is required for pause/resume (None would mean "everything" via get_jobs; avoided as a footgun).
- `run_all` still runs paused jobs (request only said run_pending skips them).
- No catch-up: a job whose next_run passed while paused runs once on first run_pending after resume.
- get_jobs_for: matches via `job.job_func.func` (partial from `Job.do`), compared with `==`
  so bound methods match.

## Failed approaches
None.

## Policy
No module-level shortcuts for new APIs (get_jobs_for, pause, resume): the project is moving off
the global default scheduler, so new APIs go on Scheduler only.
