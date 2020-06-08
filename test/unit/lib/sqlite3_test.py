import unittest

from abstract.model import User
from lib.sql_sqlite3 import SQLite3


class JSONSerializerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.db = SQLite3(memory=True)

    def tearDown(self) -> None:
        del self.db

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