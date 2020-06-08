import sqlite3
from typing import List

from abstract.database import SQLDatabase


class SQLite3(SQLDatabase):
    def __init__(self, connection_string='', memory=False):
        super().__init__()
        self.db = None
        self.last_error = None
        if memory:
            self.db = sqlite3.connect(':memory:')
        else:
            self.db = sqlite3.connect(connection_string)

    def __del__(self):
        self.db.close()

    @property
    def last_error_lazy(self):
        return self.last_error

    def select(self, sql: str, *args) -> List[tuple]:
        cur = self.db.cursor()
        try:
            cur.execute(sql, args)
            res = cur.fetchall()
        except sqlite3.DatabaseError as e:
            self.last_error = e
            res = None
        finally:
            cur.close()
        return res

    def insert(self, sql: str, *args) -> bool:
        return self.do(sql, *args)

    def create(self, sql: str, *args) -> bool:
        return self.do(sql, *args)

    def delete(self, sql: str, *args) -> bool:
        return self.do(sql, *args)

    def update(self, sql: str, *args) -> bool:
        return self.do(sql, *args)

    def do(self, sql: str, *args) -> bool:
        cur = self.db.cursor()
        try:
            cur.execute(sql, args)
            res = True
        except sqlite3.DatabaseError as e:
            self.last_error = e
            res = False
        finally:
            cur.close()
        return res
