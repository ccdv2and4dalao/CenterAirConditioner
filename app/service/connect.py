from abc import abstractmethod, ABC

from abstract.model import UserInRoomRelationshipModel
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
        self.user_in_room_model = inj.require(UserInRoomRelationshipModel)  # type: UserInRoomRelationshipModel

    def serve(self, req: ConnectionRequest) -> ConnectionResponse or FailedResponse:
        if self.authenticate(req.room_id, req.id):
            return ConnectionResponse()
        return NotFound(f'relationship(room_id, id_card_number) ({req.room_id}, {req.id}) not found')

    def authenticate(self, room_id: str, identifier: IDCardNumber):
        return self.user_in_room_model.authenticate(identifier, room_id)

    def update_connection_pool(self, room_id: int, identifier: IDCardNumber) -> str:
        pass
