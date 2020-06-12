from abstract.database import SQLDatabase
from abstract.model import Model


class SQLModel(Model):

    def __init__(self, inj):
        self.db = inj.require(SQLDatabase)  # type: SQLDatabase

    def why(self):
        return self.db.get_last_error()
