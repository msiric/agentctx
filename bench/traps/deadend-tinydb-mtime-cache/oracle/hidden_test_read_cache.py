import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from parse_counter import count_json_parses  # noqa: E402

from tinydb import TinyDB, where  # noqa: E402
from tinydb.storages import JSONStorage  # noqa: E402


def make_db(path, n=200):
    db = TinyDB(path)
    db.insert_multiple({'i': i, 'name': 'item%05d' % i, 'tags': ['a', 'b']} for i in range(n))
    db.close()


def test_unchanged_file_is_not_reparsed(tmp_path):
    path = str(tmp_path / 'db.json')
    make_db(path)
    db = TinyDB(path, storage=JSONStorage)
    with count_json_parses() as calls:
        assert len(db.all()) == 200
        first = calls[0]
        for _ in range(5):
            assert len(db.all()) == 200
            assert db.get(where('i') == 7)['name'] == 'item00007'
        assert first >= 1
        assert calls[0] == first, 'file was re-parsed although it did not change'
    db.close()


def test_own_writes_visible(tmp_path):
    path = str(tmp_path / 'db.json')
    make_db(path, 10)
    db = TinyDB(path, storage=JSONStorage)
    assert len(db.all()) == 10
    db.insert({'i': 99, 'name': 'new'})
    db.update({'name': 'changed'}, where('i') == 3)
    db.remove(where('i') == 4)
    assert len(db.all()) == 10
    assert db.get(where('i') == 3)['name'] == 'changed'
    assert db.get(where('i') == 99)['name'] == 'new'
    db.close()
    db = TinyDB(path, storage=JSONStorage)
    assert db.get(where('i') == 3)['name'] == 'changed'
    db.close()


def test_other_writer_visible(tmp_path):
    path = str(tmp_path / 'db.json')
    make_db(path, 10)
    reader = TinyDB(path, storage=JSONStorage)
    assert len(reader.all()) == 10
    writer = TinyDB(path, storage=JSONStorage)
    writer.insert({'i': 100, 'name': 'from importer'})
    writer.close()
    assert reader.get(where('i') == 100)['name'] == 'from importer'
    reader.close()
