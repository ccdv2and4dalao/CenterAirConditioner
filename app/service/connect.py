from abc import abstractmethod, ABC

from abstract.service import ConnectionService, ConnectionResponse
from app.router.flask import RouteController
from lib.injector import Injector
from proto import FailedResponse, NotFound
from proto.connection import ConnectionRequest

Identifier = str


class BaseConnectionServiceImpl(ConnectionService, ABC):

    @abstractmethod
    def authenticate(self, room_id: int, identifier: Identifier) -> str:
        pass

    @abstractmethod
    def update_connection_pool(self, room_id: int, identifier: Identifier) -> str:
        pass


class ConnectionServiceImpl(BaseConnectionServiceImpl):
    def __init__(self, _: Injector):
        pass

    def serve(self, req: ConnectionRequest) -> ConnectionResponse or FailedResponse:
        if req.room_id == '101' and req.id == '112233199911112222':
            return ConnectionResponse()
        return NotFound(f'room_id, id ({req.room_id}, {req.id}) not found')

    def authenticate(self, room_id: int, identifier: Identifier) -> str:
        pass

    def update_connection_pool(self, room_id: int, identifier: Identifier) -> str:
        pass
