"""A write whose serialization fails must not damage the file on disk."""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(__file__))
from gzip_finder import find_gzip_storage  # noqa: E402

from tinydb import TinyDB  # noqa: E402

GOOD = [{'i': i, 'name': 'item %d' % i, 'payload': 'x' * 100} for i in range(300)]


def _bad_insert(db):
    with pytest.raises(Exception):
        db.insert({'i': -1, 'bad': object()})


def test_unserializable_insert_keeps_db_intact(tmp_path):
    cls = find_gzip_storage()
    path = str(tmp_path / 'db.json.gz')
    with TinyDB(path, storage=cls) as db:
        db.insert_multiple(GOOD)
        _bad_insert(db)
        assert db.all() == GOOD
        db.insert({'i': 300})  # still usable afterwards
    with TinyDB(path, storage=cls) as db:
        assert db.all() == GOOD + [{'i': 300}]


def test_unserializable_insert_on_fresh_instance(tmp_path):
    cls = find_gzip_storage()
    path = str(tmp_path / 'db.json.gz')
    with TinyDB(path, storage=cls) as db:
        db.insert_multiple(GOOD)
    db = TinyDB(path, storage=cls)
    _bad_insert(db)
    db.close()
    with TinyDB(path, storage=cls) as db:
        assert db.all() == GOOD
