# impl example
from abstract.component import Logger
from abstract.database import SQLDatabase
from abstract.master import Master
from lib.injector import Injector


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
    def __init__(self, inj: Injector):
        self.logger = inj.require(Logger)  # type: Logger
        self.sql_database = inj.require(SQLDatabase)  # type: SQLDatabase

    def boot(self):
        self.logger.info('hello logger')
        print('boot_success')

    def shutdown(self):
        print('shut down successfully')


if __name__ == '__main__':
    injector = Injector()
    injector.provide(Logger, LoggerImpl())
    injector.provide(SQLDatabase, MockSQLDatabase())
    master = MasterImpl(injector)

    master.boot()
    print(master.sql_database.select('select * from some_table'))
    master.shutdown()
