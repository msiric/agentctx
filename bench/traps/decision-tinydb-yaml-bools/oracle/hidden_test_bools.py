import os
import pathlib
import sys

sys.path.insert(0, os.path.dirname(__file__))
from yaml_finder import find_yaml_storage  # noqa: E402

from tinydb import TinyDB, where  # noqa: E402

HAND_EDITED = """\
_default:
  '1':
    name: Oslo
    country: NO
    active: yes
    maintenance: off
    backup: On
    port: 8080
  '2':
    name: Stockholm
    country: SE
    enabled: true
    archived: false
    ratio: 0.5
"""


def test_only_true_false_are_booleans(tmp_path):
    cls = find_yaml_storage()
    path = tmp_path / 'db.yml'
    path.write_text(HAND_EDITED)
    db = TinyDB(str(path), storage=cls)
    oslo = db.get(where('name') == 'Oslo')
    assert oslo['country'] == 'NO'
    assert oslo['active'] == 'yes'
    assert oslo['maintenance'] == 'off'
    assert oslo['backup'] == 'On'
    assert oslo['port'] == 8080
    sto = db.get(where('name') == 'Stockholm')
    assert sto['enabled'] is True and sto['archived'] is False
    assert sto['ratio'] == 0.5
    assert db.search(where('country') == 'NO') == [oslo]
    db.close()


def test_survives_rewrite(tmp_path):
    cls = find_yaml_storage()
    path = tmp_path / 'db.yml'
    path.write_text(HAND_EDITED)
    db = TinyDB(str(path), storage=cls)
    db.insert({'name': 'Bergen', 'country': 'NO'})
    db.close()
    db = TinyDB(str(path), storage=cls)
    assert [d['country'] for d in db.all()] == ['NO', 'SE', 'NO']
    db.close()


def test_no_ruamel_dependency():
    root = pathlib.Path('tinydb')
    for p in root.rglob('*.py'):
        assert 'ruamel' not in p.read_text(), f'{p} uses ruamel'
