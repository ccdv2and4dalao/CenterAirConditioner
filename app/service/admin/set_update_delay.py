from typing import Union

from abstract.service.admin import AdminSetUpdateDelayService
from proto.admin.set_update_delay import AdminSetUpdateDelayRequest, AdminSetUpdateDelayResponse
from proto import FailedResponse
from abstract.component.air import MasterAirCond

class AdminSetUpdateDelayServiceImpl(AdminSetUpdateDelayService):
    def __init__(self, inj):
        self.master_air_cond = inj.require(MasterAirCond)

    def serve(self, req: AdminSetUpdateDelayRequest) -> Union[AdminSetUpdateDelayResponse, FailedResponse]:
        delay = int(req.delay)
        self.master_air_cond.update_delay = delay
        return AdminSetUpdateDelayResponse()