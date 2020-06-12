import unittest
import unittest.mock

from abstract.component import ConnectionPool
from abstract.model import UserModel, RoomModel, UserInRoomRelationshipModel
from app.server_builder import ServerBuilder
from app.service.connect import ConnectionServiceImpl
from proto import WrongPassword, ServiceCode
from proto.connection import ConnectionRequest


class BasicServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.builder = ServerBuilder(use_test_database=True)
        self.builder.build_base()
        self.builder.build_model()

    def tearDown(self) -> None:
        self.builder.close()


class ConnectionServiceTest(BasicServiceTest):
    def setUp(self) -> None:
        super().setUp()
        self.service = ConnectionServiceImpl(self.builder.injector)
        self.user1_id = None
        self.room1_id = None
        self.builder.create_table()

    def init_database_case(self):
        user_model = self.builder.injector.require(UserModel)  # type: UserModel
        room_model = self.builder.injector.require(RoomModel)  # type: RoomModel
        user_in_room_model = self.builder.injector.require(
            UserInRoomRelationshipModel)  # type: UserInRoomRelationshipModel

        self.user1_id = user_model.insert(id_card_number='user1_id')
        self.assertIsNotNone(self.user1_id, user_model.why())

        self.room1_id = room_model.insert(room_id='room1_id', app_key=self.service.password_verifier.create('1234'))
        self.assertIsNotNone(self.room1_id, room_model.why())

        x = user_in_room_model.insert(self.user1_id, self.room1_id)
        self.assertIsNotNone(x, user_in_room_model.why())

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

        def good_put(token: str, room_id: int, user_id: int, need_fan: bool):
            self.assertEqual(token, '1234')
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
