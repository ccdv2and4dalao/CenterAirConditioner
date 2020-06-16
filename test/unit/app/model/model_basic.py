import datetime
import unittest
from typing import Union

import lib.dateutil
from abstract.consensus import FanSpeed
from abstract.database import SQLDatabase
from abstract.model import EventModel, MetricModel, StatisticModel, RoomModel
from app.model import UserModelImpl, RoomModelImpl, UserInRoomRelationshipModelImpl, StatisticModelImpl, \
    MetricsModelImpl, EventModelImpl, ReportModelImpl
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


class ReportModelImplTest(BasicSqlite3Test):
    def setUp(self) -> None:
        super().setUp()

        self.start = []
        self.stop = []
        self.connect = []
        self.disconnect = []
        self.x = datetime.datetime.now()
        self.y = datetime.timedelta(seconds=1)
        self.room1_id = None  # type: Union[int, None]

        self.room_model = RoomModelImpl(self.injector)
        self.em = EventModelImpl(self.injector)
        self.mm = MetricsModelImpl(self.injector)
        self.sm = StatisticModelImpl(self.injector)

        self.injector.provide(RoomModel, self.room_model)
        self.injector.provide(EventModel, self.em)
        self.injector.provide(MetricModel, self.mm)
        self.injector.provide(StatisticModel, self.sm)
        self.rm = ReportModelImpl(self.injector)

        self.room_model.create()
        self.em.create()
        self.sm.create()
        self.mm.create()

    def now(self):
        self.x += self.y
        return self.x

    def insert_start(self, fan_speed: FanSpeed):
        em = self.em
        # self.start.append(self.now())
        d = self.now()
        self.start.append(d)
        em.insert_start_state_control_event(self.room1_id, fan_speed.value, d)
        self.assertIsNone(em.why())

    def insert_stop(self):
        em = self.em
        d = self.now()
        # self.stop.append(self.now())
        self.stop.append(d)
        em.insert_stop_state_control_event(self.room1_id, d)
        self.assertIsNone(em.why())

    def insert_connect(self):
        em = self.em
        d = self.now()
        # self.stop.append(self.now())
        self.connect.append(d)
        em.insert_connect_event(self.room1_id, d)
        self.assertIsNone(em.why())

    def insert_disconnect(self):
        em = self.em
        d = self.now()
        # self.stop.append(self.now())
        self.disconnect.append(d)
        em.insert_disconnect_event(self.room1_id, d)
        self.assertIsNone(em.why())

    def insert_data(self):
        self.room1_id = self.room_model.insert('A-101', '1234', 0)

        self.insert_connect()
        # self.insert_start(fan_speed=FanSpeed.High)
        # self.insert_stop()
        self.insert_disconnect()

    def test_get_report(self):
        self.insert_data()
        rm = self.rm
        reports, events, id2room_id = rm.get_reports(self.disconnect[0], 'day', self.room1_id)
        print(reports, events, id2room_id)

    def insert_data2(self):
        self.room1_id = self.room_model.insert('A-101', '1234', 0)

        self.insert_connect()
        self.insert_start(fan_speed=FanSpeed.High)
        self.insert_stop()
        self.insert_disconnect()

    def test_get_report2(self):
        self.insert_data2()
        rm = self.rm
        reports, events, id2room_id = rm.get_reports(self.disconnect[0], 'day', self.room1_id)
        print(reports, events, id2room_id)

    def insert_data3(self):
        self.room1_id = self.room_model.insert('A-101', '1234', 0)

        self.insert_connect()
        self.insert_start(fan_speed=FanSpeed.High)
        self.mm.insert(self.room1_id, 'high', 24.0, self.now())
        self.insert_stop()
        self.insert_disconnect()

    def test_get_report3(self):
        self.insert_data3()
        rm = self.rm
        reports, events, id2room_id = rm.get_reports(self.disconnect[0], 'day', self.room1_id)
        print(reports, events, id2room_id)


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
