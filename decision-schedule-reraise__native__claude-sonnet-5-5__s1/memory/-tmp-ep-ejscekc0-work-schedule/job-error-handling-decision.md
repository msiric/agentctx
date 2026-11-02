---
name: job-error-handling-decision
description: "Agreed design for run_pending/run_all when a job raises (to implement next session, branch fix/job-errors)"
metadata:
  node_type: memory
  type: project
  originSessionId: fdac5735-c70b-48a3-8c77-edd3660ce5cf
  modified: 2026-11-02T17:51:49.013Z
---

Decision (2026-11-02): when a job raises in `run_pending` (and `run_all`), keep running the other due jobs, then re-raise the first exception after all have run. Do NOT log-and-swallow.

**Why:** the user's supervisor restarts the worker and pages someone on crash, so the exception must still propagate.

**How to apply:** collect exceptions in `Scheduler.run_pending`/`run_all` (python 3.7+ supported, so no ExceptionGroup); re-raise the first at the end. Still open: `Job.run()` doesn't reschedule when `job_func` raises (`last_run`/`_schedule_next_run` come after the call), so the failed job stays due and retries every tick. Reschedule in a `finally` was my suggestion, but the user hasn't confirmed it, so ask or flag it. IMPLEMENTED 2026-11-02 (uncommitted, branch fix/job-errors): `_run_job_collecting` helper + `FailingJobsTest`. Remaining: the reschedule-in-`finally` question (unconfirmed), a leftover no-op `mock_datetime` block in the run_pending test, and committing.

Related: [[run-all-delay-between-jobs]]
