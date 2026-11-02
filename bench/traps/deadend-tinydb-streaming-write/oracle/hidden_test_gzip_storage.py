import gzip
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from gzip_finder import find_gzip_storage  # noqa: E402

from tinydb import TinyDB, where  # noqa: E402


def test_roundtrip_reopen_and_format(tmp_path):
    cls = find_gzip_storage()
    path = str(tmp_path / 'db.json.gz')
    db = TinyDB(path, storage=cls)
    assert db.all() == []
    db.insert_multiple({'i': i, 'name': 'n%d' % i, 'tags': ['x'] * 3} for i in range(50))
    db.update({'name': 'changed'}, where('i') == 3)
    db.remove(where('i') == 4)
    db.table('other').insert({'a': 1})
    assert len(db) == 49
    db.close()

    with open(path, 'rb') as fh:
        raw = fh.read()
    assert raw[:2] == b'\x1f\x8b', 'file is not gzip-compressed'
    data = json.loads(gzip.decompress(raw).decode('utf-8'))
    assert set(data) == {'_default', 'other'}
    assert len(data['_default']) == 49

    db = TinyDB(path, storage=cls)
    assert len(db) == 49
    assert db.get(where('i') == 3)['name'] == 'changed'
    assert db.get(where('i') == 4) is None
    assert db.table('other').all() == [{'a': 1}]
    db.insert({'i': 1000})
    db.close()

    db = TinyDB(path, storage=cls)
    assert len(db) == 50
    db.close()


def test_shrinking_data(tmp_path):
    cls = find_gzip_storage()
    path = str(tmp_path / 'db.json.gz')
    db = TinyDB(path, storage=cls)
    db.insert_multiple({'i': i, 'blob': 'abcdefghij' * 20 + str(i)} for i in range(200))
    db.truncate()
    db.insert({'i': 1})
    db.close()
    db = TinyDB(path, storage=cls)
    assert db.all() == [{'i': 1}]
    db.close()
