---
name: job-error-handling-decision
description: Agreed design for handling exceptions raised by jobs in run_pending (implemented in run_pending + Job.run, uncommitted, 2026-11-03; run_all still undecided)
metadata:
  node_type: memory
  type: project
  originSessionId: c6b5bf35-a6ec-46c4-b8e0-5bb05cbc5870
  modified: 2026-11-03T08:35:43.852Z
---

Decision (2026-11-03): when a job raises in `run_pending`, keep running the other due jobs, then re-raise the first exception once all have run. Do NOT log-and-swallow.

**Why:** the user's supervisor restarts the worker and pages someone when it crashes, so errors must still propagate.

**How to apply:** implement in `Scheduler.run_pending` (and consider `run_all`, which the user hasn't decided on). Also fix `Job.run` (`schedule/__init__.py` ~line 693): `job_func()` runs before `_schedule_next_run()`, so a failing job keeps a stale past `next_run` and retries every tick; reschedule in a `finally` or in the except path. Avoid `ExceptionGroup` unless older Python versions are handled. Branch: fix/job-errors. Built on fix/job-errors (uncommitted); test TestFailingJobs added. Remaining: run_all decision.
