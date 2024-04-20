from __future__ import annotations

import datetime
import random
import sqlite3
import typing as tp

from configs import database as database_config


T = tp.TypeVar('T', bound=tp.NamedTuple)


class Database:
    MAPPING: tp.Dict[type, str] = {
        str: "TEXT",
        float: "REAL",
        int: "INTEGER",
        datetime.datetime: "timestamp",
    }
    EL_TYPES = tp.Union[str, float, int, datetime.datetime]

    def __init__(self, database_name: str):
        self.database_name = database_name
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def create_table(self, table_name: str, columns: tp.List[tp.Tuple[str, type]]) -> None:
        field_text = ", ".join([f"{a} {self.MAPPING[b]}" for a, b in columns])

        request = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, {field_text})"

        self.cursor.execute(request)
        self.connection.commit()

    def write(self, table_name: str, columns: tp.List[EL_TYPES], data: tp.List[EL_TYPES]) -> None:
        tmp = ', '.join(['?' for _ in range(len(data))])
        request = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({tmp})"
        self.cursor.execute(request, data)
        self.connection.commit()

    def clear(self, table_name: str) -> None:
        request = f"DELETE FROM {table_name}"
        self.cursor.execute(request)
        self.connection.commit()

    def drop(self, table_name: str) -> None:
        request = f"DROP TABLE {table_name}"
        self.cursor.execute(request)
        self.connection.commit()

    def read(self, table_name: str) -> tp.List[str]:
        request = f"SELECT * FROM {table_name}"
        self.cursor.execute(request)
        res = self.cursor.fetchall()
        return res


class Table(tp.Generic[T]):
    def __init__(self, db: Database, table_name: str, row_type: tp.Type[T], temporary: bool = False):
        self.db: Database = db
        self.table_name: str = table_name
        self.row_type: tp.Type[T] = row_type
        type_hints = tp.get_type_hints(self.row_type)
        self.columns: tp.List[str] = list(type_hints.keys())
        self.db.create_table(self.table_name, list(type_hints.items()))
        self.temporary: bool = temporary

    def write(self, el: T) -> None:
        data = [getattr(el, col) for col in self.columns]
        self.db.write(self.table_name, self.columns, data)

    def clear_and_write_many(self, els: tp.List[T]) -> None:
        self.clear()
        for el in els:
            self.write(el)

    def write_tables(self, tables: tp.List[Table]) -> None:
        for table in tables:
            for el in table.read():
                self.write(el)

    def read(self) -> tp.List[T]:
        data = self.db.read(self.table_name)
        res = [self.row_type(*el[1:]) for el in data]
        return res

    def clear(self) -> None:
        self.db.clear(self.table_name)

    def __del__(self):
        if self.temporary:
            self.db.drop(self.table_name)


def create_new_table(row_type: tp.Type[T], table_name) -> Table[T]:
    table = Table(
        db=database_config.MAIN_DATABASE,
        table_name=table_name,
        row_type=row_type,
    )
    return table
