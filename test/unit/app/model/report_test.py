from abstract.model import Event, Statistic, Room, Metric
from app.model import RoomModelImpl, EventModelImpl, MetricsModelImpl, StatisticModelImpl
import unittest
from lib.injector import Injector
from abstract.database import SQLDatabase
from app.database import sqlDatabase
from sys import argv
from datetime import datetime
from time import sleep


class ReportModelTest(unittest.TestCase):
    def __init__(self):
        self.inj = Injector()
        self.db = sqlDatabase
        self.db.connect(argv[1], int(argv[2]), argv[3], argv[4], argv[5])
        self.inj.provide(SQLDatabase, self.db)


    def insert_data(self):
        r = Room(room_id='test')
        rm = RoomModelImpl(self.inj)
        rid = rm.insert(r.room_id, r.app_key)

        
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
        sleep(0.5)
        mm.insert(rid, 'high', 23.0)
        sleep(0.5)
        sm.insert(rid, 2.0, 10.0)
        sm.insert(rid, 0.2, 1.0)
        em.insert_stop_state_control_event(rid)

        em.insert_disconnect_event(rid)

if __name__ == '__main__':
        rmt = ReportModelTest()
        rmt.insert_data()
        # after insert data, generate report