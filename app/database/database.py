from typing import List, Dict, Union

from abstract.database import SQLDatabase, KVDatabase
from enum import Enum



class BaseSQLDatabaseImpl(SQLDatabase):
    def __init__(self):
        pass

    def __del__(self):
        pass

    def select(self, sql: str) -> List[tuple]:
        pass

    def insert(self, sql: str) -> bool:
        pass

    def create(self, sql: str) -> bool:
        pass

    def delete(self, sql: str) -> bool:
        pass

    def update(self, sql: str) -> bool:
        pass


class KVDatabaseImpl(KVDatabase):
    def get(self, k: str) -> object:
        pass




if __name__ == '__main__':
    Dbo = DatabaseOperation
    dbo = Dbo(None)
    print((dbo < 1).And(dbo > 4))