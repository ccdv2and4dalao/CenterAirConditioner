from abc import abstractmethod, ABC

from proto import FailedResponse, Request, Response
from proto.connection import ConnectionRequest, ConnectionResponse
from proto.metrics import MetricsResponse, MetricsRequest
from proto.start_state_control import StartStateControlRequest, StartStateControlResponse
from proto.stop_state_control import StopStateControlRequest, StopStateControlResponse


class Service(object):

    @abstractmethod
    def serve(self, req: Request) -> Response:
        pass


class ConnectionService(Service, ABC):

    @abstractmethod
    def serve(self, req: ConnectionRequest) -> ConnectionResponse or FailedResponse:
        pass


class StartStateControlService(Service, ABC):

    @abstractmethod
    def serve(self, req: StartStateControlRequest) -> StartStateControlResponse or FailedResponse:
        pass


class StopStateControlService(Service, ABC):

    @abstractmethod
    def serve(self, req: StopStateControlRequest) -> StopStateControlResponse or FailedResponse:
        pass


class MetricsService(Service, ABC):

    @abstractmethod
    def serve(self, req: MetricsRequest) -> MetricsResponse or FailedResponse:
        pass
