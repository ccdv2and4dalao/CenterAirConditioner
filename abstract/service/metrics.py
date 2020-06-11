from abc import abstractmethod, ABC

from abstract.service import Service
from proto import FailedResponse
from proto.metrics import MetricsResponse, MetricsRequest

# 8.中央空调能够实时监测各房间的温度和状态，并要求实时刷新的频率能够进行配置；

class MetricsService(Service, ABC):

    @abstractmethod
    def serve(self, req: MetricsRequest) -> MetricsResponse or FailedResponse:
        pass
