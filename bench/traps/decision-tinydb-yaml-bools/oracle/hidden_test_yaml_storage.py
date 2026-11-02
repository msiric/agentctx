import os
import sys

import yaml

sys.path.insert(0, os.path.dirname(__file__))
from yaml_finder import find_yaml_storage  # noqa: E402

from tinydb import TinyDB, where  # noqa: E402

DOC = {'none': [None, None], 'int': 42, 'float': 3.5,
       'list': ['LITE', 'RES_ACID', 'SUS_DEXT'],
       'dict': {'hp': 13, 'sp': 5},
       'bool': [True, False, True, False],
       'name': 'Bergen'}


def test_roundtrip_and_reopen(tmp_path):
    cls = find_yaml_storage()
    path = str(tmp_path / 'db.yml')
    db = TinyDB(path, storage=cls)
    assert db.all() == []
    db.insert(DOC)
    db.insert({'name': 'Oslo', 'int': 7})
    assert db.get(where('name') == 'Bergen') == DOC
    db.update({'int': 8}, where('name') == 'Oslo')
    db.remove(where('name') == 'Bergen')
    db.insert({'name': 'Trondheim', 'int': 1})
    db.close()

    with open(path) as fh:
        text = fh.read()
    assert '!' not in text, 'python-specific YAML tags in output'
    data = yaml.safe_load(text)
    assert isinstance(data, dict) and '_default' in data

    db = TinyDB(path, storage=cls)
    assert sorted(d['name'] for d in db.all()) == ['Oslo', 'Trondheim']
    assert db.get(where('name') == 'Oslo')['int'] == 8
    db.insert(DOC)
    assert db.get(where('name') == 'Bergen') == DOC
    db.close()


def test_tables(tmp_path):
    cls = find_yaml_storage()
    path = str(tmp_path / 'db.yml')
    db = TinyDB(path, storage=cls)
    db.table('cities').insert({'name': 'Oslo'})
    db.insert({'x': 1})
    db.close()
    db = TinyDB(path, storage=cls)
    assert db.tables() == {'_default', 'cities'}
    assert db.table('cities').all() == [{'name': 'Oslo'}]
    db.close()
