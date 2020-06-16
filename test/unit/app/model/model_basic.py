import datetime
import unittest

import lib.dateutil
from abstract.consensus import FanSpeed
from abstract.database import SQLDatabase
from app.model import UserModelImpl, RoomModelImpl, UserInRoomRelationshipModelImpl, StatisticModelImpl, \
    MetricsModelImpl, EventModelImpl
from lib.injector import Injector
from lib.sql_sqlite3 import SQLite3


class BasicSqlite3Test(unittest.TestCase):
    def setUp(self) -> None:
        self.db = SQLite3(memory=True)
        self.injector = Injector()
        self.injector.provide(SQLDatabase, self.db)
        self.model = None

    def tearDown(self) -> None:
        del self.db

    def assert_create_table(self):
        self.assertTrue(self.model.create(), self.db.last_error_lazy)


class UserModelImplTest(BasicSqlite3Test):
    def setUp(self) -> None:
        super().setUp()
        self.model = UserModelImpl(self.injector)

    def test_create(self):
        self.assert_create_table()

    def test_insert(self):
        self.assert_create_table()
        self.assertEqual(self.model.insert("111111202002023333"), 1, self.db.last_error_lazy)

    def test_query_by_id_card_number(self):
        self.assert_create_table()
        self.assertEqual(self.model.insert("111111202002023333"), 1, self.db.last_error_lazy)
        user = self.model.query_by_id_card_number("111111202002023333")
        self.assertIsNotNone(user, self.db.get_last_error())
        self.assertEqual(user.id, 1)
        self.assertEqual(user.id_card_number, "111111202002023333")

    def test_delete_by_id_card_number(self):
        self.assert_create_table()
        self.assertEqual(self.model.insert("111111202002023333"), 1, self.db.last_error_lazy)
        self.assertTrue(self.model.delete_by_id_card_number("111111202002023333"), self.db.last_error_lazy)
        self.assertFalse(self.model.query_by_id_card_number("111111202002023333"), self.db.last_error_lazy)


class RoomModelImplTest(BasicSqlite3Test):
    def setUp(self) -> None:
        super().setUp()
        self.model = RoomModelImpl(self.injector)

    def test_create(self):
        self.assert_create_table()

    def test_insert(self):
        self.assert_create_table()
        self.assertEqual(self.model.insert("A-101", "app_key"), 1, self.db.last_error_lazy)

    def test_query_count(self):
        self.assert_create_table()
        self.assertEqual(self.model.insert("A-101", "app_key"), 1, self.db.last_error_lazy)
        self.assertEqual(self.model.insert("A-102", "app_key"), 2, self.db.last_error_lazy)
        self.assertEqual(self.model.insert("A-103", "app_key"), 3, self.db.last_error_lazy)
        self.assertEqual(self.model.insert("A-104", "app_key"), 4, self.db.last_error_lazy)

        print(type(self.model.query_total_count()))

    def test_query_page(self):
        self.assert_create_table()
        rooms = self.model.query_page(10, 1)
        self.assertEqual(len(rooms), 0)
        self.assertEqual(self.model.insert("A-101", "app_key"), 1, self.db.last_error_lazy)
        rooms = self.model.query_page(10, 1)
        self.assertEqual(len(rooms), 1)
        self.assertEqual(rooms[0].room_id, "A-101")
        self.assertEqual(self.model.insert("A-102", "app_key"), 2, self.db.last_error_lazy)
        rooms = self.model.query_page(10, 1)
        self.assertEqual(len(rooms), 2)
        self.assertEqual(rooms[0].room_id, "A-101")
        self.assertEqual(rooms[1].room_id, "A-102")
        rooms = self.model.query_page(1, 1)
        self.assertEqual(len(rooms), 1)
        self.assertEqual(rooms[0].room_id, "A-101")
        rooms = self.model.query_page(1, 2)
        self.assertEqual(len(rooms), 1)
        self.assertEqual(rooms[0].room_id, "A-102")

    def test_query_by_id_card_number(self):
        self.assert_create_table()
        self.assertEqual(self.model.insert("A-101", "app_key"), 1, self.db.last_error_lazy)
        room = self.model.query_by_room_id("A-101")
        self.assertIsNotNone(room, self.db.get_last_error())
        self.assertEqual(room.id, 1)
        self.assertEqual(room.room_id, "A-101")
        self.assertEqual(room.app_key, "app_key")

    def test_delete_by_id_card_number(self):
        self.assert_create_table()
        self.assertEqual(self.model.insert("A-101", "app_key"), 1, self.db.last_error_lazy)
        self.assertTrue(self.model.delete_by_room_id("A-101"), self.db.last_error_lazy)
        self.assertFalse(self.model.query_by_room_id("A-101"), self.db.last_error_lazy)


class UserInRoomRelationshipModelImplTest(BasicSqlite3Test):
    def setUp(self) -> None:
        super().setUp()
        self.model = UserInRoomRelationshipModelImpl(self.injector)

    def test_create(self):
        self.assert_create_table()

    def test_insert(self):
        self.assert_create_table()
        self.assertEqual(self.model.insert(1, 1), 1, self.db.last_error_lazy)

    def test_query_exists_relationship(self):
        self.assert_create_table()
        self.assertEqual(self.model.insert(1, 1), 1, self.db.last_error_lazy)
        self.assertTrue(self.model.query(1, 1), self.db.last_error_lazy)

    def test_query_range(self):
        self.assert_create_table()
        self.assertListEqual(self.model.query_by_user_id(1), [], self.db.last_error_lazy)
        self.assertListEqual(self.model.query_by_room_id(1), [], self.db.last_error_lazy)
        self.assertEqual(self.model.insert(1, 1), 1, self.db.last_error_lazy)
        self.assertListEqual(self.model.query_by_user_id(1), [1], self.db.last_error_lazy)
        self.assertListEqual(self.model.query_by_room_id(1), [1], self.db.last_error_lazy)
        self.assertEqual(self.model.insert(1, 2), 2, self.db.last_error_lazy)
        self.assertListEqual(self.model.query_by_user_id(1), [1, 2], self.db.last_error_lazy)
        self.assertListEqual(self.model.query_by_room_id(1), [1], self.db.last_error_lazy)

    def test_query_delete(self):
        self.assert_create_table()
        self.assertEqual(self.model.insert(1, 1), 1, self.db.last_error_lazy)
        self.assertTrue(self.model.query(1, 1), self.db.last_error_lazy)
        self.assertEqual(self.model.delete(1, 1), 1, self.db.last_error_lazy)
        self.assertFalse(self.model.query(1, 1), self.db.last_error_lazy)


class StatisticModelImplTest(BasicSqlite3Test):
    def setUp(self) -> None:
        super().setUp()
        self.model = StatisticModelImpl(self.injector)

    def test_create(self):
        self.assert_create_table()

    def test_insert(self):
        self.assert_create_table()
        self.assertEqual(self.model.insert(1, 1, 1), 1, self.db.last_error_lazy)

    def test_query_by_time_interval(self):
        x = datetime.timedelta(hours=1)
        self.assert_create_table()
        res = self.model.query_by_time_interval(1, datetime.datetime.now() - x, datetime.datetime.now())
        self.assertEqual(len(res), 0)
        self.assertEqual(self.model.insert(2, 3, 4, datetime.datetime.now()), 1, self.db.last_error_lazy)
        res = self.model.query_by_time_interval(2, datetime.datetime.now() - x, datetime.datetime.now())
        self.assertEqual(len(res), 1)

        self.assertEqual(res[0].id, 1)
        self.assertEqual(res[0].room_id, 2)
        self.assertEqual(res[0].current_energy, 3)
        self.assertEqual(res[0].current_cost, 4)
        self.assertEqual(self.model.insert(2, 5, 6, datetime.datetime.now()), 2, self.db.last_error_lazy)
        res = self.model.query_by_time_interval(2, datetime.datetime.now() - x, datetime.datetime.now())
        self.assertEqual(len(res), 2)

        self.assertEqual(res[1].id, 2)
        self.assertEqual(res[1].room_id, 2)
        self.assertEqual(res[1].current_energy, 5)
        self.assertEqual(res[1].current_cost, 6)

    def test_query_sum_by_time_interval(self):
        x = datetime.timedelta(hours=1)
        self.assert_create_table()
        self.assertEqual(self.model.insert(2, 3, 4, datetime.datetime.now()), 1, self.db.last_error_lazy)
        self.assertEqual(self.model.insert(2, 5, 6, datetime.datetime.now()), 2, self.db.last_error_lazy)
        total_energy, total_cost = self.model.query_sum_by_time_interval(
            2,
            lib.dateutil.to_local(datetime.datetime.now() - x),
            lib.dateutil.to_local(datetime.datetime.now()))
        self.assertEqual(total_energy, 8)
        self.assertEqual(total_cost, 10)


class MetricsModelImplTest(BasicSqlite3Test):
    def setUp(self) -> None:
        super().setUp()
        self.model = MetricsModelImpl(self.injector)

    def test_create(self):
        self.assert_create_table()


class EventModelImplTest(BasicSqlite3Test):
    def setUp(self) -> None:
        super().setUp()
        self.model = EventModelImpl(self.injector)

    def test_create(self):
        self.assert_create_table()

    def test_insert(self):
        self.assert_create_table()
        self.assertEqual(self.model.insert_start_state_control_event(1, FanSpeed.High), 1, self.db.last_error_lazy)
        self.assertEqual(self.model.insert_stop_state_control_event(1), 2, self.db.last_error_lazy)
        self.assertEqual(self.model.insert_connect_event(1), 3, self.db.last_error_lazy)
        self.assertEqual(self.model.insert_disconnect_event(1), 4, self.db.last_error_lazy)

    def test_query_state_control_by_time_interval(self):
        x = datetime.timedelta(hours=1)
        self.assert_create_table()
        res = self.model.query_control_events_by_time_interval(1,
                                                               lib.dateutil.to_local(datetime.datetime.now() - x),
                                                               lib.dateutil.to_local(datetime.datetime.now()))
        self.assertEqual(len(res), 0)
        self.assertEqual(self.model.insert_start_state_control_event(1, FanSpeed.High, datetime.datetime.now()), 1,
                         self.db.last_error_lazy)
        res = self.model.query_control_events_by_time_interval(1,
                                                               lib.dateutil.to_local(datetime.datetime.now() - x),
                                                               lib.dateutil.to_local(datetime.datetime.now()))
        self.assertEqual(len(res), 1)
        self.assertEqual(self.model.insert_stop_state_control_event(1, datetime.datetime.now()), 2,
                         self.db.last_error_lazy)
        res = self.model.query_control_events_by_time_interval(1,
                                                               lib.dateutil.to_local(datetime.datetime.now() - x),
                                                               lib.dateutil.to_local(datetime.datetime.now()))
        self.assertEqual(len(res), 2)
        self.assertEqual(self.model.insert_connect_event(1, datetime.datetime.now()), 3, self.db.last_error_lazy)
        res = self.model.query_control_events_by_time_interval(1,
                                                               lib.dateutil.to_local(datetime.datetime.now() - x),
                                                               lib.dateutil.to_local(datetime.datetime.now()))
        self.assertEqual(len(res), 2)


if __name__ == '__main__':
    unittest.main()
