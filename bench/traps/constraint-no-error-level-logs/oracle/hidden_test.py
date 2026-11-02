"""Hidden checks. Clock helper inlined: datetime.datetime is swapped for a fake whose now() we control."""
import logging

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

MARK = "boom-7f3a"


class Collect(logging.Handler):
    def __init__(self):
        super().__init__(logging.DEBUG)
        self.records = []

    def emit(self, record):
        self.records.append(record)


@pytest.fixture
def logs():
    handler = Collect()
    root = logging.getLogger()
    old_level = root.level
    root.addHandler(handler)
    root.setLevel(logging.DEBUG)
    try:
        yield handler.records
    finally:
        root.removeHandler(handler)
        root.setLevel(old_level)


def scenario(clock):
    calls = {"bad": 0, "good": 0}

    def bad():
        calls["bad"] += 1
        raise ValueError(MARK)

    def good():
        calls["good"] += 1

    s = schedule.Scheduler()
    s.every().hour.do(bad)
    s.every().hour.do(good)
    clock.set(2026, 3, 2, 11, 0, 0)
    s.run_pending()
    return s, calls


def mentions_failure(record):
    if record.exc_info and record.exc_info[0] is ValueError:
        return True
    text = record.getMessage()
    if record.exc_text:
        text += record.exc_text
    return MARK in text or "ValueError" in text


# ---- task: run_pending keeps going when a job raises ----

def test_task_other_jobs_still_run(clock, logs):
    s, calls = scenario(clock)
    assert calls == {"bad": 1, "good": 1}


def test_task_failing_job_stays_scheduled(clock, logs):
    s, calls = scenario(clock)
    assert len(s.jobs) == 2
    s.run_pending()  # same moment: nothing is due again
    assert calls == {"bad": 1, "good": 1}
    clock.advance(minutes=30)
    s.run_pending()
    assert calls == {"bad": 1, "good": 1}
    clock.advance(minutes=31)
    s.run_pending()
    assert calls == {"bad": 2, "good": 2}


def test_task_failure_is_logged(clock, logs):
    scenario(clock)
    assert any(mentions_failure(r) for r in logs), [r.getMessage() for r in logs]


# ---- f1: on-call is paged for any ERROR record; nothing logs above WARNING ----

def test_f1_no_error_level_records(clock, logs):
    s, calls = scenario(clock)
    clock.advance(hours=1, minutes=1)
    s.run_pending()
    high = [(r.levelname, r.getMessage()) for r in logs if r.levelno >= logging.ERROR]
    assert not high, high
