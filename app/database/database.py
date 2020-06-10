from typing import List, Dict, Union

from abstract.database import SQLDatabase, KVDatabase
from enum import Enum
import pymysql
from threading import Lock

class BaseSQLDatabaseImpl(SQLDatabase):
    def __init__(self):
        self.db_lock = Lock()
        self.db = None
        self.exception = None

    def __del__(self):
        if self.db is not None:
            self.db.close()

    def connect(self, host='', port=0, user='', password='', database=''):
        with self.db_lock:
            if self.db is None:
                self.db = pymysql.connect(host=host, port=port, user=user, 
                                          password=password, database=database)
            else:
                raise RuntimeError('database has been connected')

    def select(self, sql: str, *args) -> List[tuple] or None:
        if self.db is None:
            raise RuntimeError('database should be connected before select')
        with self.db_lock:
            cursor = self.db.cursor()
            try:
                cursor.execute(sql, args)
                results = cursor.fetchall()
            except Exception as e:
                results = None
                self.exception = e
        return results

    def insert(self, sql: str, *args) -> int:
        if self.db is None:
            raise RuntimeError('database should be connected before insert')
        with self.db_lock:
            cursor = self.db.cursor()
            try:
                cursor.execute(sql, args)
                self.db.commit()
                id = cursor.lastrowid
            except Exception as e:
                self.db.rollback()
                self.exception = e
                id = -1
        return id


    def create(self, sql: str, *args) -> bool:
        if self.db is None:
            raise RuntimeError('database should be connected before create')
        with self.db_lock:
            cursor = self.db.cursor()
            try:
                cursor.execute(sql, args)
                self.db.commit()
                flag = True
            except Exception as e:
                self.db.rollback()
                self.exception = e
                flag = False
        return flag

    def delete(self, sql: str, *args) -> bool:
        if self.db is None:
            raise RuntimeError('database should be connected before delete')
        with self.db_lock:
            cursor = self.db.cursor()
            try:
                cursor.execute(sql, args)
                self.db.commit()
                flag = True
            except Exception as e:
                self.db.rollback()
                self.exception = e
                flag = False
        return flag

    def update(self, sql: str, *args) -> bool:
        if self.db is None:
            raise RuntimeError('database should be connected before update')
        with self.db_lock:
            cursor = self.db.cursor()
            try:
                cursor.execute(sql, args)
                self.db.commit()
                flag = True
            except Exception as e:
                self.db.rollback()
                self.exception = e
                flag = False
        return flag

    @property
    def last_error(self) -> Exception:
        return self.exception


sqlDatabase = BaseSQLDatabaseImpl()

class KVDatabaseImpl(KVDatabase):
    def get(self, k: str) -> object:
        pass




if __name__ == '__main__':
    '''
    SQL Database hasn't been tested!
    '''
    pass