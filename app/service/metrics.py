from abc import abstractmethod, ABC
from typing import Union

from abstract.model import MetricModel
from abstract.service import MetricsService
from lib.injector import Injector
from proto import FailedResponse
from proto.metrics import MetricsRequest, MetricsResponse


class BaseMetricsServiceImpl(MetricsService, ABC):

    @abstractmethod
    def update_metrics(self, req: MetricsRequest) -> FailedResponse or None:
        pass


class MetricsServiceImpl(BaseMetricsServiceImpl):
    def __init__(self, inj: Injector):
        self.metric_model = inj.require(MetricModel)  # type: MetricModel

    def serve(self, req) -> Union[MetricsResponse, FailedResponse]:
        self.update_metrics(req)
        return MetricsResponse()

    def update_metrics(self, req: MetricsRequest):
        self.metric_model.insert(req.room_id, req.fan_speed,
                                 req.timestamp if req.timestamp else None)
