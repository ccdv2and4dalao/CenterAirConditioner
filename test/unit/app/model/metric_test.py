import unittest
from sys import argv
from time import sleep

from abstract.database import SQLDatabase
from abstract.model import Room
from app.model import RoomModelImpl, EventModelImpl, MetricsModelImpl, StatisticModelImpl
from app.database import BaseSQLDatabaseImpl
from lib.injector import Injector


class MetricModelTest(unittest.TestCase):
    def setUp(self) -> None:
        self.inj = Injector()
        self.inj.provide(SQLDatabase, BaseSQLDatabaseImpl())
        self.db = self.inj.require(SQLDatabase)
        self.db.connect(argv[1], int(argv[2]), argv[3], argv[4], argv[5])

    def insert_data(self):
        r = Room(room_id='metric_test')
        rm = RoomModelImpl(self.inj)
        rid = rm.insert(r.room_id, r.app_key)
        r2 = Room(room_id='metric_test2')
        r2id = rm.insert(r2.room_id, r2.app_key)

        sleep(1)
        em = EventModelImpl(self.inj)
        mm = MetricsModelImpl(self.inj)
        sm = StatisticModelImpl(self.inj)
        em.insert_connect_event(rid)
        sleep(1)
        em.insert_start_state_control_event(rid, 'high')
        sleep(0.5)
        mm.insert(rid, 'high', 24.0)
        sleep(0.5)
        sm.insert(rid, 2.0, 10.0)
        em.insert_start_state_control_event(r2id, 'low')
        sleep(0.5)
        mm.insert(rid, 'high', 23.0)
        sm.insert(r2id, 1.0, 5.0)
        sleep(0.5)
        sm.insert(rid, 2.0, 10.0)
        mm.insert(r2id, 'low', 24.0)
        sm.insert(rid, 0.2, 1.0)
        em.insert_stop_state_control_event(rid)
        sleep(0.5)
        mm.insert(r2id, 'low', 23.0)
        sleep(0.5)
        em.insert_disconnect_event(rid)
        sm.insert(r2id, 1.0, 5.0)
        sleep(0.5)
        mm.insert(r2id, 'low', 22.0)
        sm.insert(r2id, 0.5, 2.5)
        em.insert_stop_state_control_event(r2id)
        sleep(1)
        em.insert_disconnect_event(r2id)



if __name__ == '__main__':
    mmt = MetricModelTest()
    mmt.setUp()
    mmt.insert_data()
    # after insert data, generate report
