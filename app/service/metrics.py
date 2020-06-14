from abc import abstractmethod, ABC
from typing import Union

from abstract.model import MetricModel
from abstract.service import MetricsService
from abstract.component import MasterAirCond
from lib.injector import Injector
from abstract.consensus import AirconTempConstraint
from proto import FailedResponse, ConflictMode, InvalidTargetTemperature
from proto.metrics import MetricsRequest, MetricsResponse


class BaseMetricsServiceImpl(MetricsService, ABC):
    @abstractmethod
    def update_metrics(self, req: MetricsRequest) -> FailedResponse or None:
        pass


class MetricsServiceImpl(BaseMetricsServiceImpl):
    def __init__(self, inj: Injector):
        self.metric_model = inj.require(MetricModel)  # type: MetricModel
        self.master_air_cond = inj.require(MasterAirCond)  # type: MasterAirCond

    def serve(self, req) -> Union[MetricsResponse, FailedResponse]:
        check_res = self.check_configuration()
        if check_res is None:
            self.update_metrics(req)
            return MetricsResponse()
        else:
            return check_res

    def check_configuration(self, req: MetricsRequest) -> FailedResponse or None:
        current_mode = self.master_air_cond.mode.value
        if req.mode != current_mode:
            return ConflictMode(f'conflict with current mode: want {current_mode}, got {req.mode}')

        if req.temperature not in AirconTempConstraint.get_contraint(req.mode):
            return InvalidTargetTemperature(f'invalid target temperature : {req.temperature}')
        else:
            return None

    def update_metrics(self, req: MetricsRequest):
        # self.metric_model.insert(req.token, req.fan_speed,
        #                         req.timestamp if req.timestamp else None)
        self.metric_model.insert(req.room_id, req.fan_speed,
                                 req.timestamp if req.timestamp else None)
