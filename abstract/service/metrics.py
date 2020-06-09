from abc import abstractmethod, ABC

from abstract.service import Service
from proto import FailedResponse
from proto.metrics import MetricsResponse, MetricsRequest


class MetricsService(Service, ABC):

    @abstractmethod
    def serve(self, req: MetricsRequest) -> MetricsResponse or FailedResponse:
        pass
