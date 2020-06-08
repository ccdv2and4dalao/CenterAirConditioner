from abc import abstractmethod, ABC

from abstract.service import Service
from proto import FailedResponse
from proto.start_state_control import StartStateControlRequest, StartStateControlResponse
from proto.stop_state_control import StopStateControlRequest, StopStateControlResponse


class StartStateControlService(Service, ABC):

    @abstractmethod
    def serve(self, req: StartStateControlRequest) -> StartStateControlResponse or FailedResponse:
        pass


class StopStateControlService(Service, ABC):

    @abstractmethod
    def serve(self, req: StopStateControlRequest) -> StopStateControlResponse or FailedResponse:
        pass
