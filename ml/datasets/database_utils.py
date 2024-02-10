import sqlite3

from typing import List, get_type_hints, Union, NamedTuple


class Database:
    MAPPING = {
        str: "TEXT",
        float: "REAL",
        int: "INTEGER",
    }
    EL_TYPES = Union[str, float, int]

    def __init__(self, database_name: str):
        self.database_name = database_name
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def create_table(self, table_name: str, columns: List[tuple[str, type]]):
        field_text = ", ".join([f"{a} {self.MAPPING[b]}" for a, b in columns])

        request = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, {field_text})"

        self.cursor.execute(request)
        self.connection.commit()

    def write(self, table_name: str, columns: List[EL_TYPES], data: List[EL_TYPES]):
        tmp = ', '.join(['?' for _ in range(len(data))])
        request = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({tmp})"
        self.cursor.execute(request, data)
        self.connection.commit()

    def clear(self, table_name: str):
        print(f"Are you sure you want to delete all data from table {table_name}? Type [y/n]")
        ans = input()
        if ans != 'y':
            print("Cancelled")
            return

        request = f"DELETE FROM {table_name}"
        self.cursor.execute(request)
        self.connection.commit()

    def read(self, table_name: str) -> List[str]:
        request = f"SELECT * FROM {table_name}"
        self.cursor.execute(request)
        res = self.cursor.fetchall()
        return res


class Dataset:
    def __init__(self, db, table_name, row_type):
        self.db = db
        self.table_name = table_name
        self.row_type = row_type
        self.columns = get_type_hints(self.row_type).keys()
        self.columns_types = get_type_hints(self.row_type).values()
        self.db.create_table(self.table_name, get_type_hints(self.row_type).items())

    def write(self, el):
        data = [getattr(el, col) for col in self.columns]
        self.db.write(self.table_name, self.columns, data)

    def read(self):
        data = self.db.read(self.table_name)
        res = [self.row_type(*el[1:]) for el in data]
        return res

    def clear(self):
        self.db.clear(self.table_name)


class FunctionDatasetRow(NamedTuple):
    function: str
    docstring: str
    docstring_score: int
    context: str


class ModelsResultsRow(NamedTuple):
    model_name: str
    prompt: str
    function: str
    docstring: str
    docstring_score: int
    context: str
