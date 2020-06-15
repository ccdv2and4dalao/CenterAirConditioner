import datetime
from abc import abstractmethod, ABC

from abstract.component import ConfigurationProvider, SystemEntropyProvider
from abstract.component.air import MasterAirCond
from abstract.component.connection_pool import ConnectionPool
from abstract.component.jwt import JWT
from abstract.component.password_verifier import PasswordVerifier
from abstract.model import UserInRoomRelationshipModel, UserModel, RoomModel, EventModel
from abstract.service import ConnectionService
from lib.injector import Injector
from proto import FailedResponse, NotFound, DatabaseError, WrongPassword, MasterAirCondNotAlive
from proto.connection import ConnectionRequest, ConnectionResponse

IDCardNumber = str


class BaseConnectionServiceImpl(ConnectionService, ABC):

    @abstractmethod
    def authenticate(self, room_id: int, identifier: IDCardNumber):
        pass

    @abstractmethod
    def update_connection_pool(self, room_id: str, identifier: IDCardNumber):
        pass


class ConnectionServiceImpl(BaseConnectionServiceImpl):
    def __init__(self, inj: Injector):
        self.user_model = inj.require(UserModel)  # type: UserModel
        self.room_model = inj.require(RoomModel)  # type: RoomModel
        self.user_in_room_model = inj.require(UserInRoomRelationshipModel)  # type: UserInRoomRelationshipModel
        self.event_model = inj.require(EventModel)  # type: EventModel
        self.cfg_provider = inj.require(ConfigurationProvider)  # type: ConfigurationProvider
        self.master_air_cond = inj.require(MasterAirCond)  # type: MasterAirCond
        self.connection_pool = inj.require(ConnectionPool)  # type: ConnectionPool
        self.password_verifier = inj.require(PasswordVerifier)  # type: PasswordVerifier
        self.jwt = inj.require(JWT)  # type: JWT
        self.random_source = inj.require(SystemEntropyProvider)  # type: SystemEntropyProvider
        self.expire_time = datetime.timedelta(hours=1)

    def serve(self, req: ConnectionRequest) -> ConnectionResponse or FailedResponse:
        ap = self.authenticate(req.room_id, req.id)
        if ap is None:
            return DatabaseError(f"database error: {self.user_in_room_model.why()}")
        if not ap:
            return NotFound(f'relationship(room_id, id_card_number) ({req.room_id}, {req.id}) not found')
        if not self.password_verifier.verify(req.app_key, ap[0]):
            return WrongPassword()
        self.update_connection_pool(ap[1], ap[2])
        response = ConnectionResponse()
        cfg = self.cfg_provider.get()
        response.token = self.jwt.create_jwt_token(
            {'room_id': ap[1], 'exp': datetime.datetime.now() + self.expire_time,
             'pd': self.random_source.get_entropy(8)})
        response.mode, response.default_temperature = self.master_air_cond.get_md_pair()
        response.mode = response.mode.value
        response.metric_delay = cfg.slave_default.metric_delay
        response.update_delay = cfg.slave_default.update_delay
        response.room_id = ap[1]
        response.user_id = ap[2]
        response.cool_min, response.cool_max = self.master_air_cond.cool_min, self.master_air_cond.cool_max
        response.heat_min, response.heat_max = self.master_air_cond.heat_min, self.master_air_cond.heat_max
        self.event_model.insert_connect_event(response.room_id)
        return response

    def authenticate(self, room_id: str, identifier: IDCardNumber):
        user = self.user_model.query_by_id_card_number(identifier)
        room = user and self.room_model.query_by_room_id(room_id)
        return room and self.user_in_room_model.query(user.id, room.id) and (room.app_key, room.id, user.id)

    def update_connection_pool(self, room_id: int, user_id: int):
        self.connection_pool.put(room_id, user_id, False)


if __name__ == '__main__':
    pass
'''
    from app.server_builder import ServerBuilder
    from abstract.database import SQLDatabase
    sb = ServerBuilder()
    sb.build()
    db = sb.injector.require(SQLDatabase)
    db.connect()

    c = sb.injector.require(ConnectionService)
    req = ConnectionRequest()
    req.room_id = 'room_test_4'
    req.id = 'user_test_4'
    req.app_key ='room_test_4'
    c.serve(req)
'''
