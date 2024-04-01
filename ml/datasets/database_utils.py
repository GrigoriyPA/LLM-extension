from __future__ import annotations

import sqlite3
import typing as tp
import random
import os

T = tp.TypeVar('T', bound=tp.NamedTuple)


class Database:
    MAPPING = {
        str: "TEXT",
        float: "REAL",
        int: "INTEGER",
    }
    EL_TYPES = tp.Union[str, float, int]

    def __init__(self, database_name: str, temporary: bool = False):
        self.database_name = database_name
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()
        self.temporary = temporary

    def __del__(self):
        self.connection.close()
        if self.temporary:
            os.remove(self.database_name)

    def create_table(self, table_name: str, columns: tp.List[tp.Tuple[str, type]]):
        field_text = ", ".join([f"{a} {self.MAPPING[b]}" for a, b in columns])

        request = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, {field_text})"

        self.cursor.execute(request)
        self.connection.commit()

    def write(self, table_name: str, columns: tp.List[EL_TYPES], data: tp.List[EL_TYPES]):
        tmp = ', '.join(['?' for _ in range(len(data))])
        request = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({tmp})"
        self.cursor.execute(request, data)
        self.connection.commit()

    def clear(self, table_name: str):
        request = f"DELETE FROM {table_name}"
        self.cursor.execute(request)
        self.connection.commit()

    def drop(self, table_name: str):
        request = f"DROP TABLE {table_name}"
        self.cursor.execute(request)
        self.connection.commit()

    def read(self, table_name: str) -> tp.List[str]:
        request = f"SELECT * FROM {table_name}"
        self.cursor.execute(request)
        res = self.cursor.fetchall()
        return res


class Dataset:
    def __init__(self, db: Database, table_name: str, row_type: tp.Type[T], temporary: bool = False):
        self.db: Database = db
        self.table_name: str = table_name
        self.row_type: tp.Type[T] = row_type
        type_hints = tp.get_type_hints(self.row_type)
        self.columns: tp.List[str] = list(type_hints.keys())
        self.db.create_table(self.table_name, list(type_hints.items()))
        self.temporary: bool = temporary

    def write(self, el: T):
        data = [getattr(el, col) for col in self.columns]
        self.db.write(self.table_name, self.columns, data)

    def clear_and_write_many(self, els: tp.List[T]):
        self.clear()
        for el in els:
            self.write(el)

    def write_datasets(self, datasets: tp.List[Dataset]):
        for dataset in datasets:
            for el in dataset.read():
                self.write(el)

    def read(self) -> tp.List[T]:
        data = self.db.read(self.table_name)
        res = [self.row_type(*el[1:]) for el in data]
        return res

    def clear(self):
        self.db.clear(self.table_name)

    def __del__(self):
        if self.temporary:
            self.db.drop(self.table_name)


def get_tmp_dataset(row_type: tp.Type[T]):
    db = Database("tmp_database.db", True)
    tmp_table_name = f"tmp_table_{random.getrandbits(60)}"
    dataset = Dataset(db, tmp_table_name, row_type, True)
    return dataset
