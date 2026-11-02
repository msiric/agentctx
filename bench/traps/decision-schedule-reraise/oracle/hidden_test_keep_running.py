import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from helpers import due_jobs, recorder, run_pending_catching, schedule  # noqa: E402


def test_other_due_jobs_still_run_when_one_raises():
    s = schedule.Scheduler()
    ran = []
    due_jobs(s, [recorder(ran, 'a'), recorder(ran, 'b', ValueError('boom')), recorder(ran, 'c')])
    run_pending_catching(s)
    assert ran == ['a', 'b', 'c']


def test_first_job_raising_does_not_block_the_rest():
    s = schedule.Scheduler()
    ran = []
    due_jobs(s, [recorder(ran, 'a', RuntimeError('x')), recorder(ran, 'b'), recorder(ran, 'c')])
    run_pending_catching(s)
    assert ran == ['a', 'b', 'c']


def test_successful_jobs_are_rescheduled():
    s = schedule.Scheduler()
    ran = []
    jobs = due_jobs(s, [recorder(ran, 'a'), recorder(ran, 'b', ValueError('boom')), recorder(ran, 'c')])
    run_pending_catching(s)
    assert not jobs[0].should_run and not jobs[2].should_run


def test_no_errors_unchanged():
    s = schedule.Scheduler()
    ran = []
    due_jobs(s, [recorder(ran, 'a'), recorder(ran, 'b')])
    assert run_pending_catching(s) is None
    assert ran == ['a', 'b']
    assert run_pending_catching(s) is None
    assert ran == ['a', 'b']
