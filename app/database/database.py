from typing import List, Dict, Union

from abstract.database import SQLDatabase, KVDatabase
from enum import Enum
import pymysql
from threading import Lock

class BaseSQLDatabaseImpl(SQLDatabase):
    def __init__(self):
        self.db_lock = Lock()
        self.db = None

    def __del__(self):
        if self.db is not None:
            self.db.close()

    def connect(host='', user='', password='', database=''):
        with self.db_lock:
            if self.db is None:
                self.db = pymysql.connect(host, user, password, database)
            else:
                raise RuntimeError('database has been connected')

    def select(self, sql: str) -> List[tuple] or None:
        if self.db is None:
            raise RuntimeError('database should be connected before select')
        with self.db_lock:
            cursor = self.db.cursor()
            try:
                cursor.execute(sql)
                results = cursor.fetchall()
            except:
                results = None
        return results

    def insert(self, sql: str) -> bool:
        if self.db is None:
            raise RuntimeError('database should be connected before insert')
        with self.db_lock:
            cursor = self.db.cursor()
            try:
                cursor.execute(sql)
                self.db.commit()
                flag = True
            except:
                self.db.rollback()
                flag = False
        return flag


    def create(self, sql: str) -> bool:
        if self.db is None:
            raise RuntimeError('database should be connected before create')
        with self.db_lock:
            cursor = self.db.cursor()
            try:
                cursor.execute(sql)
                self.db.commit()
                flag = True
            except:
                self.db.rollback()
                flag = False
        return flag

    def delete(self, sql: str) -> bool:
        if self.db is None:
            raise RuntimeError('database should be connected before delete')
        with self.db_lock:
            cursor = self.db.cursor()
            try:
                cursor.execute(sql)
                self.db.commit()
                flag = True
            except:
                self.db.rollback()
                flag = False
        return flag

    def update(self, sql: str) -> bool:
        if self.db is None:
            raise RuntimeError('database should be connected before update')
        with self.db_lock:
            cursor = self.db.cursor()
            try:
                cursor.execute(sql)
                self.db.commit()
                flag = True
            except:
                self.db.rollback()
                flag = False
        return flag


sqlDatabase = BaseSQLDatabaseImpl()

class KVDatabaseImpl(KVDatabase):
    def get(self, k: str) -> object:
        pass




if __name__ == '__main__':
    '''
    SQL Database hasn't been tested!
    '''
    pass