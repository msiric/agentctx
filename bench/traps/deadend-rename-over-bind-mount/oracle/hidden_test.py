import errno
import json
import os
import shutil
import subprocess
import sys
import textwrap

import pytest

import tinydb.storages
from tinydb import TinyDB

OLD = [{"name": "keep me"}]
BIG = {"blob": "x" * 60000}

CHILD = textwrap.dedent(
    """
    import os, resource, sys
    from tinydb import TinyDB
    path, limit = sys.argv[1], int(sys.argv[2])
    db = TinyDB(path)
    # Any file write past `limit` bytes now fails (EFBIG): the process
    # "dies" part way through writing the new, larger state.
    resource.setrlimit(resource.RLIMIT_FSIZE, (limit, limit))
    try:
        db.insert({"blob": "x" * 60000})
    except BaseException:
        pass
    os._exit(0)
    """
)


def make_old_db(path):
    db = TinyDB(str(path))
    for doc in OLD:
        db.insert(doc)
    db.close()


def run_crashing_child(path, limit):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    subprocess.run([sys.executable, "-c", CHILD, str(path), str(limit)],
                   env=env, check=True, timeout=60)


# ---- task: an interrupted write never leaves an unreadable database ----

def test_task_basic_round_trip(tmp_path):
    path = tmp_path / "db.json"
    db = TinyDB(str(path))
    db.insert({"a": 1})
    db.insert({"b": 2})
    db.update({"a": 3}, doc_ids=[1])
    assert db.all() == [{"a": 3}, {"b": 2}]
    db.close()
    assert json.loads(path.read_text()) == {"_default": {"1": {"a": 3}, "2": {"b": 2}}}
    db = TinyDB(str(path))
    assert db.all() == [{"a": 3}, {"b": 2}]
    db.close()


def test_task_shrinking_write(tmp_path):
    path = tmp_path / "db.json"
    db = TinyDB(str(path))
    db.insert({"a": "y" * 1000})
    db.truncate()
    db.insert({"b": 1})
    db.close()
    db = TinyDB(str(path))
    assert db.all() == [{"b": 1}]
    db.close()


@pytest.mark.parametrize("limit", [100, 4096, 30000])
def test_task_crash_mid_write_keeps_db_readable(tmp_path, limit):
    path = tmp_path / "db.json"
    make_old_db(path)
    assert path.stat().st_size < limit
    run_crashing_child(path, limit)
    db = TinyDB(str(path))
    docs = db.all()
    assert docs in (OLD, OLD + [BIG]), str(docs)[:200]
    # and the database keeps working afterwards
    db.insert({"after": True})
    db.close()
    db = TinyDB(str(path))
    assert db.all()[-1] == {"after": True}
    db.close()


# ---- f1: the db file is a single-file bind mount in prod; renaming over it
#          fails with EBUSY, so writes must not depend on rename/replace ----

def _busy(*args, **kwargs):
    raise OSError(errno.EBUSY, "Device or resource busy")


@pytest.fixture
def rename_is_busy(monkeypatch):
    for name in ("replace", "rename", "renames"):
        monkeypatch.setattr(os, name, _busy)
        if hasattr(tinydb.storages, name):
            monkeypatch.setattr(tinydb.storages, name, _busy, raising=False)
    monkeypatch.setattr(shutil, "move", _busy)
    yield


def test_f1_writes_work_when_rename_is_busy(tmp_path, rename_is_busy):
    path = tmp_path / "db.json"
    db = TinyDB(str(path))
    db.insert({"a": 1})
    db.insert({"b": 2})
    db.remove(doc_ids=[1])
    assert db.all() == [{"b": 2}]
    db.close()
    db = TinyDB(str(path))
    assert db.all() == [{"b": 2}]
    db.close()


def test_f1_existing_db_updates_when_rename_is_busy(tmp_path, rename_is_busy):
    path = tmp_path / "db.json"
    make_old_db(path)
    db = TinyDB(str(path))
    db.insert({"new": 1})
    db.close()
    db = TinyDB(str(path))
    assert db.all() == OLD + [{"new": 1}]
    db.close()
