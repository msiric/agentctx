"""Decision from session 1: run the other due jobs, then re-raise the first error
(the supervisor relies on the crash to restart the worker and page someone)."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from helpers import due_jobs, flatten, recorder, run_pending_catching, schedule  # noqa: E402


def test_error_is_reraised_after_other_jobs_ran():
    s = schedule.Scheduler()
    ran = []
    err = ValueError('boom')
    due_jobs(s, [recorder(ran, 'a'), recorder(ran, 'b', err), recorder(ran, 'c')])
    exc = run_pending_catching(s)
    assert exc is not None, 'run_pending swallowed the job error'
    assert ran == ['a', 'b', 'c']
    assert err in flatten(exc) or isinstance(exc, ValueError)


def test_first_error_wins():
    s = schedule.Scheduler()
    ran = []
    first, second = KeyError('first'), RuntimeError('second')
    due_jobs(s, [recorder(ran, 'a', first), recorder(ran, 'b'), recorder(ran, 'c', second)])
    exc = run_pending_catching(s)
    assert exc is not None, 'run_pending swallowed the job errors'
    assert ran == ['a', 'b', 'c']
    flat = flatten(exc)
    if isinstance(exc, BaseExceptionGroup):
        assert first in flat
    else:
        assert exc is first or isinstance(exc, KeyError)


def test_module_level_run_pending_reraises_too():
    schedule.clear()
    ran = []
    try:
        due_jobs(schedule.default_scheduler,
                 [recorder(ran, 'a', ValueError('x')), recorder(ran, 'b')])
        try:
            schedule.run_pending()
        except BaseException as e:  # noqa: B902
            assert any(isinstance(x, ValueError) for x in flatten(e))
        else:
            raise AssertionError('schedule.run_pending swallowed the job error')
        assert ran == ['a', 'b']
    finally:
        schedule.clear()
