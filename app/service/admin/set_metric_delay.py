from typing import Union

from abstract.component.air import MasterAirCond
from abstract.service.admin import AdminSetMetricDelayService
from proto import FailedResponse
from proto.admin.set_metric_delay import AdminSetMetricDelayRequest, AdminSetMetricDelayResponse


class AdminSetMetricDelayServiceImpl(AdminSetMetricDelayService):
    def __init__(self, inj):
        self.master_air_cond = inj.require(MasterAirCond)  # type: MasterAirCond

    def serve(self, req: AdminSetMetricDelayRequest) -> Union[AdminSetMetricDelayResponse, FailedResponse]:
        self.master_air_cond.metric_delay = req.delay
        return AdminSetMetricDelayResponse()
