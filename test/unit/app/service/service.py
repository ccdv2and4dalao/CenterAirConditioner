import unittest
import unittest.mock
from datetime import datetime, timedelta

from abstract.component import ConnectionPool
from abstract.component.password_verifier import PasswordVerifier
from abstract.consensus import FanSpeed
from abstract.model import UserModel, RoomModel, UserInRoomRelationshipModel, EventModel, StatisticModel
from app.server_builder import ServerBuilder
from app.service.admin.get_slave_statistics_v2 import AdminGetSlaveStatisticsServiceImplV2
from app.service.connect import ConnectionServiceImpl
from app.service.metrics import MetricsServiceImpl
from app.service.start_state_control import StartStateControlServiceImpl
from lib.dateutil import now
from proto import WrongPassword, ServiceCode
from proto.admin.get_slave_statistics import AdminGetSlaveStatisticsRequest
from proto.connection import ConnectionRequest
from proto.metrics import MetricsRequest
from proto.start_state_control import StartStateControlRequest


class BasicServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.builder = ServerBuilder(use_test_database=True)
        self.builder.build_base()
        self.builder.build_model()
        self.user1_id = None
        self.room1_id = None
        self.builder.create_table()

    def tearDown(self) -> None:
        self.builder.close()

    def init_database_case(self):
        user_model = self.builder.injector.require(UserModel)  # type: UserModel
        room_model = self.builder.injector.require(RoomModel)  # type: RoomModel
        password_verifier = self.builder.injector.require(PasswordVerifier)  # type: PasswordVerifier
        user_in_room_model = self.builder.injector.require(
            UserInRoomRelationshipModel)  # type: UserInRoomRelationshipModel

        self.user1_id = user_model.insert(id_card_number='user1_id')
        self.assertIsNotNone(self.user1_id, user_model.why())

        self.room1_id = room_model.insert(room_id='room1_id', app_key=password_verifier.create('1234'))
        self.assertIsNotNone(self.room1_id, room_model.why())

        x = user_in_room_model.insert(self.user1_id, self.room1_id)
        self.assertIsNotNone(x, user_in_room_model.why())


class ConnectionServiceTest(BasicServiceTest):
    def setUp(self) -> None:
        super().setUp()
        self.service = ConnectionServiceImpl(self.builder.injector)

    def test_connect(self):
        self.init_database_case()

        # example 1

        req = ConnectionRequest()
        req.room_id = 'room1_id'
        req.id = 'user1_id'
        req.app_key = '1234'

        connection_pool = unittest.mock.Mock(spec=ConnectionPool)
        self.service.connection_pool = connection_pool

        # self.connection_pool.put(token, room_id, user_id, False)

        def good_put(room_id: int, user_id: int, need_fan: bool):
            self.assertEqual(room_id, self.user1_id)
            self.assertEqual(user_id, self.room1_id)
            self.assertFalse(need_fan)
            return None

        connection_pool.put = unittest.mock.Mock(side_effect=good_put)

        resp = self.service.serve(req)
        mode, default_temperature = self.service.master_air_cond.get_md_pair()
        mode = mode.value
        metric_delay = self.service.cfg_provider.get().slave_default.metric_delay
        update_delay = self.service.cfg_provider.get().slave_default.update_delay

        self.assertEqual(resp.code, 0)
        self.assertEqual(resp.default_temperature, default_temperature)
        self.assertEqual(resp.mode, mode)
        self.assertEqual(resp.metric_delay, metric_delay)
        self.assertEqual(resp.update_delay, update_delay)
        self.assertEqual(resp.user_id, self.user1_id)
        self.assertEqual(resp.room_id, self.room1_id)

        # example 2

        req = ConnectionRequest()
        req.room_id = 'room1_id'
        req.id = 'user1_id'
        req.app_key = '1233'

        def bad_put(*_):
            self.fail('should not put connection pool')

        connection_pool.put = unittest.mock.Mock(side_effect=bad_put)

        resp = self.service.serve(req)
        self.assertIsInstance(resp, WrongPassword)
        self.assertEqual(resp.code, ServiceCode.WrongPassword.value)


class StartStateControlServiceImplTest(BasicServiceTest):

    def setUp(self) -> None:
        super().setUp()
        self.service = StartStateControlServiceImpl(self.builder.injector)

    def test_start_state_control(self):
        req = StartStateControlRequest()

        # assuming connection is in pool
        connection_pool = self.builder.injector.require(ConnectionPool)  # type: ConnectionPool
        connection_pool.put(self.user1_id, self.room1_id, False)

        req.token = '1234'
        req.room_id = self.room1_id
        req.mode = 'cool'
        req.speed = 'high'
        resp = self.service.serve(req)
        self.assertEqual(resp.code, 0, resp)


class MetricsServiceImplTest(BasicServiceTest):
    def setUp(self) -> None:
        super().setUp()
        self.service = MetricsServiceImpl(self.builder.injector)
        self.builder.create_table()

    def test_metrics(self):
        req = MetricsRequest()

        # assuming connection is in pool
        connection_pool = self.builder.injector.require(ConnectionPool)  # type: ConnectionPool
        connection_pool.put(self.user1_id, self.room1_id, False)

        # test case 1
        req.token = '1234'
        req.mode = 'cool'
        req.fan_speed = 'low'
        req.temperature = 25.1
        checkpoint = now()
        resp = self.service.serve(req)

        self.assertEqual(resp.code, 8)

        # test case 1
        req.token = '1234'
        req.room_id = self.room1_id
        req.mode = 'heat'
        req.fan_speed = 'low'
        req.temperature = 25.1
        checkpoint = now()
        resp = self.service.serve(req)

        self.assertEqual(resp.code, 2)

        # test case 2
        req.token = '1234'
        req.room_id = self.room1_id
        req.mode = 'cool'
        req.fan_speed = 'high'
        req.temperature = 24.9
        checkpoint = now()
        resp = self.service.serve(req)

        self.assertEqual(resp.code, 0)


class GetSlaveStatisticsServiceV2Test(BasicServiceTest):

    def setUp(self) -> None:
        super().setUp()
        self.service = AdminGetSlaveStatisticsServiceImplV2(self.builder.injector)

        self.start = []
        self.stop = []
        self.room1_id = 1
        self.x = datetime.now()
        self.y = timedelta(seconds=1)
        self.init_database_case()

    def now(self):
        self.x += self.y
        return self.x

    def insert_start(self, fan_speed: FanSpeed):
        em = self.builder.injector.require(EventModel)  # type: EventModel
        # self.start.append(self.now())
        d = self.now()
        self.start.append(d)
        em.insert_start_state_control_event(self.room1_id, fan_speed.value, d)
        self.assertIsNone(em.why())

    def insert_stop(self):
        em = self.builder.injector.require(EventModel)  # type: EventModel
        d = self.now()
        # self.stop.append(self.now())
        self.stop.append(d)
        em.insert_stop_state_control_event(self.room1_id, d)
        self.assertIsNone(em.why())

    def init_database_case(self):
        sm = self.builder.injector.require(StatisticModel)  # type: StatisticModel

        self.insert_start(FanSpeed.High)
        sm.insert(self.room1_id, 1, 2, self.now())
        self.assertIsNone(sm.why())
        sm.insert(self.room1_id, 3, 4, self.now())
        self.assertIsNone(sm.why())
        self.insert_stop()

        self.insert_start(FanSpeed.Mid)
        sm.insert(self.room1_id, 4, 7, self.now())
        self.assertIsNone(sm.why())
        sm.insert(self.room1_id, 9, 9, self.now())
        self.assertIsNone(sm.why())
        self.insert_stop()

        self.insert_start(FanSpeed.Low)
        self.insert_stop()

        self.insert_start(FanSpeed.Low)
        self.stop.append(self.now())
        # self.insert_stop()

        self.start.append(self.now())
        self.insert_stop()

    # noinspection DuplicatedCode
    def test_get_slave_statistics_v2(self):
        req = AdminGetSlaveStatisticsRequest()
        req.room_id = self.room1_id
        req.start_time = self.start[0]
        req.stop_time = self.stop[0]

        resp = self.service.serve(req)
        self.assertEqual(resp.code, 0, resp.__dict__)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['energy'], 4)
        self.assertEqual(resp.data[0]['cost'], 6)

        req.room_id = self.room1_id
        req.start_time = self.start[0]
        req.stop_time = self.stop[1]

        resp = self.service.serve(req)
        self.assertEqual(resp.code, 0, resp.__dict__)
        self.assertEqual(len(resp.data), 2)
        self.assertEqual(resp.data[0]['energy'], 4)
        self.assertEqual(resp.data[0]['cost'], 6)
        self.assertEqual(resp.data[1]['energy'], 13)
        self.assertEqual(resp.data[1]['cost'], 16)

        req.room_id = self.room1_id
        req.start_time = self.start[1]
        req.stop_time = self.stop[1]

        resp = self.service.serve(req)
        self.assertEqual(resp.code, 0, resp.__dict__)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['energy'], 13)
        self.assertEqual(resp.data[0]['cost'], 16)

        req.room_id = self.room1_id
        req.start_time = self.start[0]
        req.stop_time = self.stop[2]

        resp = self.service.serve(req)
        self.assertEqual(resp.code, 0, resp.__dict__)
        self.assertEqual(len(resp.data), 3)
        self.assertEqual(resp.data[0]['energy'], 4)
        self.assertEqual(resp.data[0]['cost'], 6)
        self.assertEqual(resp.data[1]['energy'], 13)
        self.assertEqual(resp.data[1]['cost'], 16)
        self.assertEqual(resp.data[2]['energy'], 0)
        self.assertEqual(resp.data[2]['cost'], 0)

        req.room_id = self.room1_id
        req.start_time = self.start[2]
        req.stop_time = self.stop[2]

        resp = self.service.serve(req)
        self.assertEqual(resp.code, 0, resp.__dict__)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['energy'], 0)
        self.assertEqual(resp.data[0]['cost'], 0)

        req.room_id = self.room1_id
        req.start_time = self.start[3]
        req.stop_time = self.stop[3]

        resp = self.service.serve(req)
        self.assertEqual(resp.code, 0, resp.__dict__)
        self.assertEqual(len(resp.data), 0)

        req.room_id = self.room1_id
        req.start_time = self.start[4]
        req.stop_time = self.stop[4]

        resp = self.service.serve(req)
        self.assertEqual(resp.code, 0, resp.__dict__)
        self.assertEqual(len(resp.data), 0)


if __name__ == '__main__':
    unittest.main()
