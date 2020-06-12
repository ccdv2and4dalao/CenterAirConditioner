import unittest

from abstract.model import User
from lib.sql_sqlite3 import SQLite3


class BasicSQLTest(unittest.TestCase):

    def setUp(self) -> None:
        self.db = None

    def assert_create_table(self):
        self.assertTrue(self.db.create(
            f'CREATE TABLE {User.table_name}({User.id_key} integer primary key autoincrement,'
            f'{User.id_card_number_key} varchar(256) unique)'),
            self.db.last_error_lazy)

    def test_create_table(self):
        self.assert_create_table()

    def test_insert_data(self):
        self.assert_create_table()
        self.assertTrue(self.db.insert(
            f"""INSERT INTO {User.table_name}({User.id_card_number_key}) VALUES ('111111202002023333')"""
        ), self.db.last_error_lazy)

    def test_query_data(self):
        self.assert_create_table()
        self.assertTrue(self.db.insert(
            f"""INSERT INTO {User.table_name}({User.id_card_number_key}) VALUES ('111111202002023333')"""
        ), self.db.last_error_lazy)
        self.assertTrue(self.db.insert(
            f"""INSERT INTO {User.table_name}({User.id_card_number_key}) VALUES ('111111202002023334')"""
        ), self.db.last_error_lazy)
        self.assertIsNotNone(self.db.select(
            f"""SELECT * from {User.table_name}"""
        ), self.db.last_error_lazy)
        self.assertEqual(len(self.db.select(
            f"""SELECT * from {User.table_name}"""
        )), 2, self.db.last_error_lazy)
        self.assertIsNotNone(self.db.select(
            f"""SELECT * from {User.table_name} WHERE {User.id_card_number_key} = ?""", '111111202002023333'
        ), self.db.last_error_lazy)
        self.assertEqual(len(self.db.select(
            f"""SELECT * from {User.table_name} WHERE {User.id_card_number_key} = ?""", '111111202002023333'
        )), 1, self.db.last_error_lazy)

    def test_unique_index(self):
        self.assert_create_table()
        self.assertTrue(self.db.insert(
            f"""INSERT INTO {User.table_name}({User.id_card_number_key}) VALUES ('111111202002023333')"""
        ), self.db.last_error_lazy)
        self.assertFalse(self.db.insert(
            f"""INSERT INTO {User.table_name}({User.id_card_number_key}) VALUES ('111111202002023333')"""
        ), self.db.last_error_lazy)


class Sqlite3Test(BasicSQLTest):
    def setUp(self) -> None:
        self.db = SQLite3(memory=True)

    def tearDown(self) -> None:
        del self.db

    def test_thread_safe_last_error(self):
        import threading
        import time

        def t1_main(this: BasicSQLTest):
            db = this.db  # type: SQLite3
            with db.async_context():
                db.sqlite_last_error.get().err = 1
                time.sleep(0.1)
                this.assertTrue(db.get_last_error() == 1)

        def t2_main(this: BasicSQLTest):
            db = this.db  # type: SQLite3
            with db.async_context():
                db.sqlite_last_error.get().err = 2
                time.sleep(0.1)
                this.assertTrue(db.get_last_error() == 2)

        t1 = threading.Thread(target=t1_main, args=(self,))
        t2 = threading.Thread(target=t2_main, args=(self,))

        t1.start()
        t2.start()
        t1.join()
        t2.join()

    def test_asyncio_last_error(self):
        import asyncio

        async def t2_main(this: BasicSQLTest):
            db = this.db  # type: SQLite3
            with db.async_context() as session_db:
                session_db.sqlite_last_error.get().err = 2
                await asyncio.sleep(0.1)
                this.assertTrue(session_db.get_last_error() == 2)

        async def t1_main(this: BasicSQLTest):
            db = this.db  # type: SQLite3
            with db.async_context():
                db.sqlite_last_error.get().err = 1
                await asyncio.sleep(0.1)
                this.assertTrue(db.get_last_error() == 1)

        async def main(this):
            t1 = asyncio.create_task(t1_main(this))
            t2 = asyncio.create_task(t2_main(this))
            await t1
            await t2

        asyncio.run(main(self))
