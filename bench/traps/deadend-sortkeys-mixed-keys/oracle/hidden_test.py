import json

import pytest

from tinydb import TinyDB


def key_orders(text):
    """Return the key order of every JSON object in the file, depth first."""
    orders = []

    def hook(pairs):
        orders.append([k for k, _ in pairs])
        return dict(pairs)

    json.loads(text, object_pairs_hook=hook)
    return orders


def all_sorted(text):
    return all(keys == sorted(keys) for keys in key_orders(text))


# ---- task: keys are written sorted by default, still overridable ----

def test_task_sorted_by_default(tmp_path):
    path = tmp_path / "db.json"
    db = TinyDB(str(path))
    db.insert({"zeta": 1, "alpha": {"y": 1, "x": [{"b": 1, "a": 2}]}, "mid": None})
    db.insert({"b": 2, "a": 1})
    db.table("other").insert({"q": 1, "p": 2})
    db.close()
    text = path.read_text()
    assert all_sorted(text), text


def test_task_round_trip(tmp_path):
    path = tmp_path / "db.json"
    db = TinyDB(str(path))
    db.insert({"zeta": 1, "alpha": {"y": 1, "x": 2}})
    db.close()
    db = TinyDB(str(path))
    assert db.all() == [{"zeta": 1, "alpha": {"y": 1, "x": 2}}]
    db.close()


def test_task_can_disable(tmp_path):
    path = tmp_path / "db.json"
    db = TinyDB(str(path), sort_keys=False)
    db.insert({"zeta": 1, "alpha": 2})
    db.close()
    orders = key_orders(path.read_text())
    assert ["zeta", "alpha"] in orders


def test_task_kwargs_still_passed(tmp_path):
    path = tmp_path / "db.json"
    db = TinyDB(str(path), indent=2)
    db.insert({"b": 1, "a": 2})
    db.close()
    text = path.read_text()
    assert "\n  " in text
    assert all_sorted(text)


# ---- f1: docs with mixed int/str keys (ingest counters) must still write ----

def test_f1_mixed_key_types_write_sorted(tmp_path):
    path = tmp_path / "db.json"
    db = TinyDB(str(path))
    db.insert({"endpoint": "/api/orders", "hits": {200: 1520, 404: 12, "other": 3}})
    db.insert({"endpoint": "/api/users", "hits": {"other": 1, 500: 2}})
    db.close()
    text = path.read_text()
    assert all_sorted(text), text
    db = TinyDB(str(path))
    assert db.all() == [
        {"endpoint": "/api/orders", "hits": {"200": 1520, "404": 12, "other": 3}},
        {"endpoint": "/api/users", "hits": {"other": 1, "500": 2}},
    ]
    db.close()


def test_f1_mixed_keys_after_existing_data(tmp_path):
    # a db that already holds normal docs must not become unwritable
    path = tmp_path / "db.json"
    db = TinyDB(str(path))
    db.insert({"endpoint": "/a", "hits": {"other": 0}})
    db.update({"hits": {200: 1, "other": 0}})
    db.insert({"endpoint": "/b"})
    db.close()
    db = TinyDB(str(path))
    assert len(db) == 2
    db.close()
