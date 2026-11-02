"""On the NFS share mtime has 1-second resolution: a write by another process
within the same second leaves mtime unchanged. Simulate that by restoring the
mtime after the other process's write (file size is unchanged too)."""
import os

from tinydb import TinyDB, where
from tinydb.storages import JSONStorage


def _write_same_second(path, mutate):
    st = os.stat(path)
    other = TinyDB(path, storage=JSONStorage)
    mutate(other)
    other.close()
    assert os.path.getsize(path) == st.st_size
    os.utime(path, ns=(st.st_atime_ns, st.st_mtime_ns))


def test_same_second_same_size_write_is_seen(tmp_path):
    path = str(tmp_path / 'db.json')
    db = TinyDB(path)
    db.insert_multiple([{'sku': 'A-1', 'status': 'open'}, {'sku': 'B-2', 'status': 'open'}])
    db.close()

    reader = TinyDB(path, storage=JSONStorage)
    assert reader.get(where('sku') == 'A-1')['status'] == 'open'

    _write_same_second(path, lambda o: o.update({'status': 'shut'}, where('sku') == 'A-1'))

    assert reader.get(where('sku') == 'A-1')['status'] == 'shut'
    assert reader.count(where('status') == 'open') == 1
    reader.close()


def test_same_second_write_after_own_write_is_seen(tmp_path):
    path = str(tmp_path / 'db.json')
    db = TinyDB(path)
    db.insert({'sku': 'A-1', 'qty': 10})
    db.close()

    reader = TinyDB(path, storage=JSONStorage)
    reader.update({'qty': 11}, where('sku') == 'A-1')
    assert reader.get(where('sku') == 'A-1')['qty'] == 11

    _write_same_second(path, lambda o: o.update({'qty': 12}, where('sku') == 'A-1'))

    assert reader.get(where('sku') == 'A-1')['qty'] == 12
    reader.close()
