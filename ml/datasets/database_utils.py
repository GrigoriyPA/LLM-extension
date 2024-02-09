import sqlite3

from typing import List
from abc import abstractmethod, ABC


class BaseDatabase:
    def __init__(self, database_name: str):
        self.database_name = database_name
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def create_table(self, table_name: str, columns: List[tuple[str, str]]):
        for a, b in columns:
            assert b in ['TEXT', 'REAL', 'INTEGER']
        field_text = ", ".join([f"{a} {b}" for a, b in columns])

        request = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, {field_text})"
        self.cursor.execute(request)
        self.connection.commit()

    def write_data(self, table_name: str, columns: List[str], data: List[str]):
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

    def get_data(self, table_name: str) -> List[str]:
        request = f"SELECT * FROM {table_name}"
        self.cursor.execute(request)
        res = self.cursor.fetchall()
        return res


class AbstractDataset(ABC):
    @abstractmethod
    def write_el(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_data(self, *args, **kwargs):
        pass

    @abstractmethod
    def clear(self):
        pass


class FunctionsDataset(AbstractDataset):
    table_name = "functions_docstrings"
    columns = ["function", "docstring", "docstring_score", "context"]
    columns_type = ["TEXT", "TEXT", "INTEGER", "TEXT"]

    def __init__(self, db):
        self.db = db
        self.db.create_table(self.table_name, [(a, b) for a, b in zip(self.columns, self.columns_type)])

    def write_el(self, function: str, docstring: str, docstring_score: int, context: str = ""):
        data = [function, docstring, docstring_score, context]
        self.db.write_data(self.table_name, self.columns, data)

    def get_data(self):
        return self.db.get_data(self.table_name)

    def clear(self):
        self.db.clear(self.table_name)


class ModelsResultsDataset(AbstractDataset):
    table_name = "models_results"
    columns = ["model_name", "prompt", "function", "docstring", "docstring_score", "context"]
    columns_type = ["TEXT", "TEXT", "TEXT", "TEXT", "INTEGER", "TEXT"]

    def __init__(self, db):
        self.db = db
        self.db.create_table(self.table_name, [(a, b) for a, b in zip(self.columns, self.columns_type)])

    def write_el(self, model_name: str, prompt: str, function: str, docstring: str, docstring_score: int, context: str):
        data = [model_name, prompt, function, docstring, docstring_score, context]
        self.db.write_data(self.table_name, self.columns, data)

    def get_data(self):
        return self.db.get_data(self.table_name)

    def clear(self):
        self.db.clear(self.table_name)

# func_ds = FunctionsDataset('main.db')
# func_ds.write_el("def sum(a: int, b: int) -> int:\n\treturn a + b",
#  "calculates sum of two given numbers a + b and returns it", 10, "z = sum(x, y)")
