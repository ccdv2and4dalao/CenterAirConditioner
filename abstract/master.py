from abc import abstractmethod

from abstract.database import SQLDatabase
from lib.injector import Injector
from abstract.component.logger import Logger


class Master(object):

    def __init__(self, inj: Injector):
        self.logger = inj.require(Logger)  # type: Logger
        self.sql_database = inj.require(SQLDatabase)  # type: SQLDatabase

    @abstractmethod
    def bootMaster(self):
        pass


if __name__ == '__main__':
    # impl example
    class LoggerImpl(Logger):

        def info(self, msg: str):
            print(msg)

        def warn(self, msg: str):
            pass

        def debug(self, msg: str):
            pass

        def error(self, msg: str):
            pass

        def fatal(self, msg: str):
            pass

    class MockSQLDatabase(SQLDatabase):
        def select(self, sql: str):
            return [tuple([1, 'a mock row'])]

    class MasterImpl(Master):
        def bootMaster(self):
            self.logger.info('hello logger')
            print('boot_success')


    injector = Injector()
    injector.provide(Logger, LoggerImpl())
    injector.provide(SQLDatabase, MockSQLDatabase())
    master = MasterImpl(injector)

    master.bootMaster()
    print(master.sql_database.select('select * from some_table'))


