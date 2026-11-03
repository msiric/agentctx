---
name: job-error-handling-decision
description: Agreed design for run_pending/run_all when a job raises (branch fix/job-errors); implemented 2026-11-03 (uncommitted)
metadata:
  node_type: memory
  type: project
  originSessionId: 65e12a55-9c67-49b4-a212-471990c2fd70
  modified: 2026-11-03T01:59:08.114Z
---

Decision (2026-11-03): when a job raises in `run_pending` (and `run_all`), keep running the other due jobs, then re-raise the first exception after all have run. Do NOT log-and-swallow.

**Why:** the user's supervisor restarts the worker and pages someone on crash, so failures must still propagate.

**How to apply:** implement on branch fix/job-errors. Also check `_run_job` reschedules (`_schedule_next_run`) even when the job raises, so a failing job doesn't stay perpetually due. Cover both `run_pending` and `run_all`. Add tests. User said to build it in the next session.

Related: `run_all` delay-only-between-jobs change was done earlier the same day (uncommitted, no dedicated test).
