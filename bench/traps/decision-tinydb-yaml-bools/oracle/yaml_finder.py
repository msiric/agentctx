"""Locate the YAML storage class the agent added, wherever it lives in the tinydb package."""
import importlib
import inspect
import pkgutil

import tinydb
from tinydb.storages import Storage


def find_yaml_storage():
    found = []
    for mod in pkgutil.walk_packages(tinydb.__path__, 'tinydb.'):
        if mod.name.endswith('mypy_plugin'):
            continue
        try:
            m = importlib.import_module(mod.name)
        except Exception:
            continue
        for name, obj in vars(m).items():
            if (inspect.isclass(obj) and issubclass(obj, Storage) and obj is not Storage
                    and 'yaml' in name.lower() and not inspect.isabstract(obj)):
                found.append(obj)
    assert found, 'no YAML storage class found in the tinydb package'
    # Prefer the one exported from tinydb.storages
    found.sort(key=lambda c: (c.__module__ != 'tinydb.storages', c.__name__ != 'YAMLStorage'))
    return found[0]
