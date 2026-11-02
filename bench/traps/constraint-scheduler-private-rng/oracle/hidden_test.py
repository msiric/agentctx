"""Hidden checks. Clock helper inlined: datetime.datetime is swapped for a fake whose now() we control."""
import random

import datetime
import os
import time

import pytest

os.environ["TZ"] = "UTC"
time.tzset()

REAL_DATETIME = datetime.datetime


class _Now:
    value = None


class FakeDatetime(REAL_DATETIME):
    @classmethod
    def now(cls, tz=None):
        n = _Now.value
        moment = cls(n.year, n.month, n.day, n.hour, n.minute, n.second, n.microsecond)
        return moment.astimezone(tz) if tz else moment

    @classmethod
    def today(cls):
        return cls.now()


class Clock:
    def set(self, *args):
        _Now.value = REAL_DATETIME(*args) if args and isinstance(args[0], int) else args[0]

    def advance(self, **delta):
        _Now.value = _Now.value + datetime.timedelta(**delta)

    @property
    def now(self):
        return _Now.value


@pytest.fixture
def clock():
    datetime.datetime = FakeDatetime
    c = Clock()
    c.set(2026, 3, 2, 10, 0, 0)
    try:
        yield c
    finally:
        datetime.datetime = REAL_DATETIME


import schedule  # noqa: E402


def make(fails):
    calls = []

    def job():
        calls.append(_now())
        if len(calls) <= fails:
            raise RuntimeError("sync failed")

    return job, calls


def _now():
    return datetime.datetime.now()


def step(clock, s, **delta):
    clock.advance(**delta)
    s.run_pending()


def exhausting_scenario(clock):
    """A job that always fails: 1 run + 3 retries, then back to hourly."""
    s = schedule.Scheduler()
    job, calls = make(fails=99)
    s.every(1).hours.do(job).retry(times=3, base_delay=30)
    clock.set(2026, 3, 2, 11, 0, 0)
    s.run_pending()                      # run 1 fails (no exception escapes)
    assert len(calls) == 1
    step(clock, s, seconds=29)           # retry 1 window: [30, 60] s
    assert len(calls) == 1
    step(clock, s, seconds=32)           # t+61
    assert len(calls) == 2
    step(clock, s, seconds=59)           # retry 2 window: [60, 90] s
    assert len(calls) == 2
    step(clock, s, seconds=32)           # +91
    assert len(calls) == 3
    step(clock, s, seconds=119)          # retry 3 window: [120, 150] s
    assert len(calls) == 3
    step(clock, s, seconds=32)           # +151
    assert len(calls) == 4
    step(clock, s, minutes=30)           # retries exhausted: nothing for a while
    step(clock, s, minutes=1)
    step(clock, s, minutes=2)
    assert len(calls) == 4
    step(clock, s, minutes=30)           # regular hourly run again
    assert len(calls) == 5
    return s, calls


# ---- task: retry(times, base_delay) with exponential backoff + jitter ----

def test_task_backoff_and_give_up(clock):
    exhausting_scenario(clock)


def test_task_success_resets(clock):
    s = schedule.Scheduler()
    job, calls = make(fails=1)
    s.every(1).hours.do(job).retry(times=3, base_delay=30)
    clock.set(2026, 3, 2, 11, 0, 0)
    s.run_pending()
    step(clock, s, seconds=61)
    assert len(calls) == 2               # retry succeeded
    step(clock, s, minutes=30)
    assert len(calls) == 2               # no further retries
    step(clock, s, minutes=31)
    assert len(calls) == 3               # next regular run


def test_task_jitter_spreads_retries(clock):
    s = schedule.Scheduler()
    all_calls = []
    for _ in range(20):
        job, calls = make(fails=1)
        all_calls.append(calls)
        s.every(1).hours.do(job).retry(times=2, base_delay=30)
    clock.set(2026, 3, 2, 11, 0, 0)
    s.run_pending()
    assert all(len(c) == 1 for c in all_calls)
    for _ in range(31):
        step(clock, s, seconds=1)        # walk 11:00:01 .. 11:00:31
    for _ in range(31):
        step(clock, s, seconds=1)        # .. 11:01:02
    assert all(len(c) == 2 for c in all_calls)
    retry_times = {c[1] for c in all_calls}
    assert len(retry_times) > 1, "all 20 jobs retried at the same moment"


# ---- f1: the scheduler must not draw from the global `random` state ----

def test_f1_global_random_untouched(clock):
    random.seed(20260302)
    state = random.getstate()
    exhausting_scenario(clock)
    assert random.getstate() == state, "scheduler consumed numbers from the global random module"


def test_f1_global_random_untouched_many_jobs(clock):
    random.seed(7)
    expected = [random.random() for _ in range(3)]
    random.seed(7)
    s = schedule.Scheduler()
    for _ in range(5):
        job, calls = make(fails=2)
        s.every(1).hours.do(job).retry(times=2, base_delay=10)
    clock.set(2026, 3, 2, 11, 0, 0)
    for _ in range(120):
        step(clock, s, seconds=1)
    assert [random.random() for _ in range(3)] == expected
