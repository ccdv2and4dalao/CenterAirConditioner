from typing import List, Dict, Union

from abstract.database import SQLDatabase, KVDatabase
from enum import Enum


class DatabaseType(Enum):
    default = ''
    int = 'INTEGER'
    pass

class DatabaseTerm:
    def __init__(self, name: str, t: DatabaseType=DatabaseType.default, 
                 table='',
                 length=0, is_null=True, 
                 is_primary_key=False, foreign=None,):
        pass

    def __str__(self):
        pass

class DatabaseOperation:
    def __init__(self, term: DatabaseTerm):
        pass

    def __str__(self):
        return ''

    def __lt__(self, rhs):
        # do something and return a DatabaseOperation
        pass

    def __le__(self, rhs):
        pass

    def __gt__(self, rhs):
        pass

    def __ge__(self, rhs):
        pass

    def __eq__(self, rhs):
        pass

    def __ne__(self, rhs):
        pass

    def And(self, op):
        pass

    def Or(self, op):
        pass

    def Between(self, cond1, cond2):
        pass

    def Not(self):
        pass

class BaseSQLDatabaseImpl(SQLDatabase):
    def __init__(self):
        pass

    def __del__(self):
        pass

    def _select(self, sql: str) -> List[tuple]:
        pass

    def select(self, cols: List[str], table: str, conditions: Union[str, DatabaseOperation]='', 
               join: Dict[str, Union[str, DatabaseOperation]]={}, order=None, limit=None) -> List[tuple]:
        pass

    def select_sql(self, sql: str) -> List[tuple]:
        '''
        In case that self.select cannot support all the situations, this function can be used
to write sql directly.
        '''
        pass

    def _insert(self, sql: str) -> bool:
        pass

    def insert(self, table: str, terms: Dict[str, List[str]]) -> bool:
        pass

    def _create(self, sql: str) -> bool:
        pass

    def create(self, table: str, terms: List[DatabaseTerm]) -> bool:
        pass

    def _delete(self, sql: str) -> bool:
        pass

    def delete(self, table: str, conditions: Union[str, DatabaseOperation]='') -> bool:
        pass

    def _update(self, sql: str) -> bool:
        pass

    def update(self, table: str, sets: Union[str, DatabaseOperation], 
               conditions: Union[str, DatabaseOperation]='') -> bool:
        pass

class KVDatabaseImpl(KVDatabase):
    def get(self, k: str) -> object:
        pass




if __name__ == '__main__':
    Dbo = DatabaseOperation
    dbo = Dbo(None)
    print((dbo < 1).And(dbo > 4))