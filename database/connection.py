from enums import Gender
from .sql import *

import datetime as dt
from pathlib import Path
import sqlite3
from sqlite3 import Connection


def custom_type_date():
    def adapt(date: dt.date) -> str:
        return date.isoformat()

    def convert(b: bytes) -> dt.date:
        return dt.date.fromisoformat(b.decode())

    sqlite3.register_adapter(dt.date, adapt)
    sqlite3.register_converter("date", convert)


def custom_type_datetime():
    def adapt(datetime: dt.datetime) -> str:
        return datetime.isoformat()

    def convert(b: bytes) -> dt.datetime:
        return dt.datetime.fromisoformat(b.decode())

    sqlite3.register_adapter(dt.datetime, adapt)
    sqlite3.register_converter("timestamp", convert)


def custom_type_gender():
    def adapt(gender: Gender) -> int:
        return gender.value

    def convert(b: bytes) -> Gender:
        return Gender(int(b))

    sqlite3.register_adapter(Gender, adapt)
    sqlite3.register_converter("GENDER", convert)


custom_type_date()
custom_type_datetime()
custom_type_gender()


def create_connection(path: Path) -> Connection:
    con = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")
    con.execute("UPDATE singleton SET last_open_date = date('now')")
    con.commit()
    return con


def close_connection(con: Connection):
    con.execute("PRAGMA optimize")
    con.close()


def init_database(con: Connection):
    con.executescript(create_table_sql)
    con.executescript(create_index_sql)
    con.executescript(create_view_sql)
    con.executescript(create_trigger_sql)
    con.executescript(finalized_sql)


def insert[T: BASEMODEL](con: Connection, t: type[T], data: Mapping[str, Any]) -> int:
    with con:
        cur = con.execute(
            f"""
            INSERT INTO {t.__tablename__} ({t.commna_joined_fields()})
            VALUES ({t.named_style_placeholders()})
        """,
            data,
        )
        assert cur.lastrowid is not None
        return cur.lastrowid


def select[T: BASEMODEL](con: Connection, t: type[T], id: int) -> T | None:
    row = con.execute(f"SELECT * FROM {t.__tablename__} WHERE id={id}").fetchone()
    if row is None:
        return None
    else:
        return t.parse(row)


def selectall[T: BASEMODEL](con: Connection, t: type[T]) -> dict[int, T]:
    rows = con.execute(f" SELECT * FROM {t.__tablename__}").fetchall()
    return {row["id"]: t.parse(row) for row in rows}


def delete[T: BASEMODEL](con: Connection, t: type[T], id: int):
    with con:
        rowcount = con.execute(
            f"DELETE FROM {t.__tablename__} WHERE id = {id}"
        ).rowcount
        assert rowcount == 1, "delete should be success"


def update[T: BASEMODEL](con: Connection, t: type[T], id: int, data: Mapping[str, Any]):
    with con:
        rowcount = con.execute(
            f"""
            UPDATE {t.__tablename__} SET ({t.commna_joined_fields()})
            = ({t.named_style_placeholders()})
            WHERE id = {id}
        """,
            data,
        ).rowcount
        assert rowcount == 1, "update should be success"
