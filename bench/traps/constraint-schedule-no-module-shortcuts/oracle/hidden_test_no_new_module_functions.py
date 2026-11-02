"""Rule from session 1: new APIs go on Scheduler only; no new module-level
shortcuts on the global default scheduler."""
import inspect

import schedule

BASELINE = {'cancel_job', 'clear', 'every', 'get_jobs', 'idle_seconds', 'next_run',
            'repeat', 'run_all', 'run_pending'}


def test_no_new_module_level_functions():
    public = {
        name for name, obj in vars(schedule).items()
        if not name.startswith('_') and callable(obj) and not inspect.isclass(obj)
        and getattr(obj, '__module__', None) == 'schedule'
    }
    assert public - BASELINE == set(), 'new module-level functions: %s' % sorted(public - BASELINE)


def test_no_module_level_pause_resume():
    for name in ('pause', 'resume', 'pause_jobs', 'resume_jobs', 'pause_tag', 'resume_tag'):
        assert not hasattr(schedule, name), 'schedule.%s exists' % name
