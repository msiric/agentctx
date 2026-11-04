---
name: no-new-module-level-shortcuts
description: New APIs go only on Scheduler; no new module-level shortcuts for the default scheduler
metadata:
  type: feedback
---

Add new public APIs only as `Scheduler` methods; do not add module-level wrappers that call `default_scheduler`.

**Why:** The team is moving everyone off the global default scheduler.

**How to apply:** When adding a feature in `schedule/__init__.py`, skip the module-level function; in tests call `schedule.default_scheduler.<method>` or use a `Scheduler()` instance.
