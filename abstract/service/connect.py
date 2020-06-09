from abc import ABC, abstractmethod

from abstract.service import Service
from proto import FailedResponse
from proto.connection import ConnectionRequest, ConnectionResponse


class ConnectionService(Service, ABC):

    @abstractmethod
    def serve(self, req: ConnectionRequest) -> ConnectionResponse or FailedResponse:
        pass
