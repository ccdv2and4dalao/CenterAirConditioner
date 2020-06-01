from abc import abstractmethod, ABC

from abstract.service import MetricsService
from proto import FailedResponse
from proto.metricsrequest import MetricsRequest


class BaseMetricsServiceImpl(MetricsService, ABC):

    @abstractmethod
    def update_metrics(self, req: MetricsRequest) -> FailedResponse or None:
        pass
