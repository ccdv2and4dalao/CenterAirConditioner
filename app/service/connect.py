from abc import abstractmethod, ABC

from abstract.service import ConnectionService

Identifier = str


class BaseConnectionServiceImpl(ConnectionService, ABC):

    @abstractmethod
    def authenticate(self, room_id: int, identifier: Identifier) -> str:
        pass

    @abstractmethod
    def update_connection_pool(self, room_id: int, identifier: Identifier) -> str:
        pass
