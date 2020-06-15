from typing import Union

from abstract.service.admin import AdminSetMetricDelayService
from proto.admin.set_metric_delay import AdminSetMetricDelayRequest, AdminSetMetricDelayResponse
from proto import FailedResponse
from abstract.component.air import MasterAirCond

class AdminSetMetricDelayServiceImpl(AdminSetMetricDelayService):
    def __init__(self, inj):
        self.master_air_cond = inj.require(MasterAirCond)

    def serve(self, req: AdminSetMetricDelayRequest) -> Union[AdminSetMetricDelayResponse, FailedResponse]:
        delay = int(req.delay)
        self.master_air_cond.metric_delay = delay
        return AdminSetMetricDelayResponse()
