from typing import List

from abstract.database import SQLDatabase, KVDatabase


class SQLDatabaseImpl(SQLDatabase):
    def select(self, sql: str) -> List[tuple]:
        pass


class KVDatabaseImpl(KVDatabase):
    def get(self, k: str) -> object:
        pass


