from collections.abc import Iterable
from sqlite3 import Connection
from pathlib import Path
from typing import Any
from dataclasses import fields
from itertools import chain

from lib.models import BASEMODEL
from ._custom_types import *

custom_type_datetime()
custom_type_gender()


def connect(path: Path) -> Connection:
    conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    return conn


def _process_misc(
    t: BASEMODEL, misc: dict[str, Any] | None = None
) -> tuple[Iterable[str], dict[str, Any]]:
    if misc is None:
        field_names = [f.name for f in fields(t)]
        value = {attr.name: getattr(t, attr.name) for attr in fields(t)}
    else:
        field_names = list(chain((f.name for f in fields(t)), ("misc",)))
        value = {attr.name: getattr(t, attr.name) for attr in fields(t)} | {
            "misc": misc
        }
    return (field_names, value)


def insert(conn: Connection, t: BASEMODEL, misc: dict[str, Any] | None = None) -> int:
    with conn:
        field_names, value = _process_misc(t, misc)
        cur = conn.execute(
            f"""
            INSERT INTO {t.__tablename__} ({",".join(field_names)})
            VALUES ({",".join(f":{f}" for f in field_names)})
        """,
            value,
        )
        assert cur.lastrowid is not None, "insert should be successful"
        return cur.lastrowid


def update(conn: Connection, t: BASEMODEL, id: int, misc: dict[str, Any] | None = None):
    with conn:
        field_names, value = _process_misc(t, misc)
        rowcount = conn.execute(
            f"""
            UPDATE {t.__tablename__} SET ({",".join(field_names)})
            = ({",".join(f":{f}" for f in field_names)})
            WHERE id = {id}
        """,
            value,
        ).rowcount
        assert rowcount == 1, "update should be successful"


def delete(conn: Connection, t: type[BASEMODEL], id: int):
    with conn:
        rowcount = conn.execute(
            f"DELETE FROM {t.__tablename__} WHERE id = {id}"
        ).rowcount
        assert rowcount == 1, "delete should be success"
