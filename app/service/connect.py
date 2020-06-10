from abc import abstractmethod, ABC

from abstract.component import ConfigurationProvider
from abstract.model import UserInRoomRelationshipModel, UserModel, RoomModel
from abstract.service import ConnectionService
from lib.injector import Injector
from proto import FailedResponse, NotFound
from proto.connection import ConnectionRequest, ConnectionResponse

IDCardNumber = str


class BaseConnectionServiceImpl(ConnectionService, ABC):

    @abstractmethod
    def authenticate(self, room_id: int, identifier: IDCardNumber):
        pass

    @abstractmethod
    def update_connection_pool(self, room_id: int, identifier: IDCardNumber):
        pass


class ConnectionServiceImpl(BaseConnectionServiceImpl):
    def __init__(self, inj: Injector):
        self.user_model = inj.require(UserModel)  # type: UserModel
        self.room_model = inj.require(RoomModel)  # type: RoomModel
        self.user_in_room_model = inj.require(UserInRoomRelationshipModel)  # type: UserInRoomRelationshipModel
        self.cfg_provider = inj.require(ConfigurationProvider)  # type: ConfigurationProvider

    def serve(self, req: ConnectionRequest) -> ConnectionResponse or FailedResponse:
        if self.authenticate(req.room_id, req.id):
            response = ConnectionResponse()
            cfg = self.cfg_provider.get()
            response.default_temperature = cfg.slave_default.default_temperature
            response.metric_delay = cfg.slave_default.metric_delay
            response.update_delay = cfg.slave_default.update_delay
            response.mode = cfg.slave_default.mode
            return response
        return NotFound(f'relationship(room_id, id_card_number) ({req.room_id}, {req.id}) not found')

    def authenticate(self, room_id: str, identifier: IDCardNumber):
        user = self.user_model.query_by_id_card_number(identifier)
        room = user and self.room_model.query_by_room_id(room_id)
        return room and self.user_in_room_model.query(user.id, room.id)

    def update_connection_pool(self, room_id: int, identifier: IDCardNumber) -> str:
        pass
