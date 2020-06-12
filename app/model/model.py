from abstract.database import SQLDatabase
from lib.serializer import Serializer
from abstract.model import Model


class SQLModel(Model):

    def __init__(self, inj):
        self.db = inj.require(SQLDatabase)  # type: SQLDatabase

    def why(self):
        return self.db.get_last_error()

    def select_1(self, table_name, key, value):
        data = self.db.select(f'''
        select * from {table_name} where {key} = {self.db.placeholder}
        ''', value)
        if data is None:
            return None
        if len(data) == 0:
            return False
        return data
