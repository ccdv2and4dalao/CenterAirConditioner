from abc import ABC, abstractmethod

from abstract.service import Service
from proto import FailedResponse
from proto.disconnect import DisConnectionRequest, DisConnectionResponse


class DisConnectionService(Service, ABC):
    @abstractmethod
    def serve(self, req: DisConnectionRequest) -> DisConnectionResponse or FailedResponse:
        pass
