import contextvars
import sqlite3
from typing import List

from abstract.database import SQLDatabase
from lib.async_context import AsyncContext


class SqliteLastErrorRef(object):

    def __init__(self):
        self.err = None


class SQLite3(AsyncContext, SQLDatabase):
    sqlite_last_error: contextvars.ContextVar

    def connect(self, host='', port=0, user='', password='', database=''):
        pass

    def __init__(self, connection_string='', memory=False):
        super().__init__(SqliteLastErrorRef, ref_name='sqlite_last_error')
        self.db = None
        if memory:
            self.db = sqlite3.connect(':memory:')
        else:
            self.db = sqlite3.connect(connection_string)

    def __del__(self):
        self.db.close()

    def get_last_error(self) -> Exception:
        return self.sqlite_last_error.get().err

    @property
    def last_error_lazy(self):
        return self.sqlite_last_error.get().err

    def select(self, sql: str, *args) -> List[tuple]:
        cur = self.db.cursor()
        try:
            cur.execute(sql, args)
            res = cur.fetchall()
        except sqlite3.DatabaseError as e:
            self.sqlite_last_error.get().err = e
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
            self.sqlite_last_error.get().err = e
            res = False
        finally:
            cur.close()
        return res
