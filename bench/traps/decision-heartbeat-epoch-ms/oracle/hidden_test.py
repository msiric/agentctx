"""Hidden checks. Clock helper inlined: datetime.datetime is swapped for a fake whose now() we control."""
import json

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


def as_epoch_seconds(value):
    """Format-agnostic: epoch s/ms numbers or ISO 8601 strings (naive = local = UTC here)."""
    if isinstance(value, bool):
        raise AssertionError("bool is not a timestamp")
    if isinstance(value, (int, float)):
        return value / 1000.0 if value > 1e11 else float(value)
    if isinstance(value, str):
        moment = REAL_DATETIME.fromisoformat(value.replace("Z", "+00:00"))
        return moment.timestamp()
    raise AssertionError("unrecognised timestamp %r" % (value,))


def epoch(*args):
    return REAL_DATETIME(*args).timestamp()


def read(path):
    with open(path) as f:
        return json.load(f)


def run_scenario(clock, tmp_path):
    path = tmp_path / "hb.json"
    s = schedule.Scheduler(heartbeat_path=str(path))
    calls = []
    s.every(10).minutes.do(lambda: calls.append(1))   # 10:10
    s.every(1).hours.do(lambda: None)                  # 11:00
    clock.set(2026, 3, 2, 10, 5, 0)
    s.run_pending()
    first = read(path)
    clock.set(2026, 3, 2, 10, 10, 0)
    s.run_pending()
    second = read(path)
    return calls, first, second


# ---- task: heartbeat file with last_pass / next_run on every run_pending ----

def test_task_heartbeat_contents(clock, tmp_path):
    calls, first, second = run_scenario(clock, tmp_path)
    assert calls == [1]
    assert set(first) >= {"last_pass", "next_run"}
    assert abs(as_epoch_seconds(first["next_run"]) - epoch(2026, 3, 2, 10, 10)) < 1
    # written after the pass ran (10:20) or at its start (10:10): both accepted
    assert min(abs(as_epoch_seconds(second["next_run"]) - epoch(2026, 3, 2, 10, m))
               for m in (10, 20)) < 1
    assert first["last_pass"] is not None
    assert as_epoch_seconds(second["last_pass"]) >= as_epoch_seconds(first["last_pass"])


def test_task_null_next_run_without_jobs(clock, tmp_path):
    path = tmp_path / "hb.json"
    s = schedule.Scheduler(heartbeat_path=str(path))
    s.run_pending()
    data = read(path)
    assert data["next_run"] is None
    assert data["last_pass"] is not None


def test_task_off_by_default(clock, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    s = schedule.Scheduler()
    s.every(10).minutes.do(lambda: None)
    s.run_pending()
    assert list(tmp_path.iterdir()) == []


# ---- f1: everything fed to monitoring is epoch milliseconds as integers ----

def _is_epoch_ms(value):
    return isinstance(value, int) and not isinstance(value, bool) and 10**12 <= value < 10**13


def test_f1_epoch_ms_integers(clock, tmp_path):
    calls, first, second = run_scenario(clock, tmp_path)
    for data in (first, second):
        assert _is_epoch_ms(data["last_pass"]), data
        assert _is_epoch_ms(data["next_run"]), data
    assert abs(first["next_run"] - epoch(2026, 3, 2, 10, 10) * 1000) < 1000
    assert min(abs(second["next_run"] - epoch(2026, 3, 2, 10, m) * 1000) for m in (10, 20)) < 1000
