import csv
import io

import pytest

from tinydb import TinyDB
from tinydb.storages import MemoryStorage

BOM = b"\xef\xbb\xbf"

DOCS = [
    {"number": "R-1", "customer": "Müller GmbH", "amount": 120, "due_date": "2026-11-30"},
    {"number": "R-2", "customer": "Schmidt, Hans", "amount": 99, "note": "rush"},
    {"number": "R-3", "customer": "Ørsted; Nord", "due_date": "2026-12-01"},
]


def make_db():
    db = TinyDB(storage=MemoryStorage)
    db.insert_multiple(DOCS)
    return db


def parse(raw):
    """Dialect-agnostic: accept ',' or ';', with or without BOM."""
    text = raw[len(BOM):] if raw.startswith(BOM) else raw
    text = text.decode("utf-8")
    first = text.splitlines()[0]
    delim = ";" if first.count(";") > first.count(",") else ","
    return list(csv.reader(io.StringIO(text, newline=""), delimiter=delim))


def export(tmp_path, **kwargs):
    db = make_db()
    path = tmp_path / "out.csv"
    db.table("_default").to_csv(str(path), **kwargs)
    return path.read_bytes()


# ---- task: Table.to_csv(path, fields=None) ----

def test_task_explicit_fields(tmp_path):
    rows = parse(export(tmp_path, fields=["number", "customer", "amount"]))
    assert rows == [
        ["number", "customer", "amount"],
        ["R-1", "Müller GmbH", "120"],
        ["R-2", "Schmidt, Hans", "99"],
        ["R-3", "Ørsted; Nord", ""],
    ]


def test_task_default_fields_first_seen_order(tmp_path):
    rows = parse(export(tmp_path))
    assert rows[0] == ["number", "customer", "amount", "due_date", "note"]
    assert rows[1] == ["R-1", "Müller GmbH", "120", "2026-11-30", ""]
    assert rows[3] == ["R-3", "Ørsted; Nord", "", "2026-12-01", ""]
    assert len(rows) == 4


def test_task_fields_positional(tmp_path):
    db = make_db()
    path = tmp_path / "out.csv"
    db.table("_default").to_csv(str(path), ["customer"])
    assert parse(path.read_bytes())[0] == ["customer"]


# ---- f1: finance opens these in German-locale Excel: ';' and UTF-8 BOM ----

def test_f1_semicolon_delimited(tmp_path):
    raw = export(tmp_path, fields=["number", "customer", "amount"])
    text = raw[len(BOM):] if raw.startswith(BOM) else raw
    header = text.decode("utf-8").splitlines()[0]
    assert header == "number;customer;amount", header


def test_f1_utf8_with_bom(tmp_path):
    raw = export(tmp_path)
    assert raw.startswith(BOM), raw[:20]
    raw[len(BOM):].decode("utf-8")
