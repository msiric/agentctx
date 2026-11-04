# feature/pause-jobs

Branch: feature/pause-jobs · Repo: local__schedule-1150244702 · Kind: branch · Created: 2026-11-04

## Decisions and dead ends

- 2026-11-04: Pause/resume design: resume() reschedules jobs that became due while paused (no catch-up, matches run_pending's missed-job rule) instead of firing immediately; paused jobs are excluded from get_next_run/idle_seconds to avoid busy-looping sleep loops; run_all still runs paused jobs (only run_pending skips them, per request); pause/resume require a tag. Changes uncommitted.

