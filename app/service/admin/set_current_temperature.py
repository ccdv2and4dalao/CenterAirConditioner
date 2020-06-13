from abstract.component import MasterAirCond
from abstract.service.admin.set_current_temperature import AdminSetCurrentTemperatureService
from proto import FailedResponse
from proto.admin.set_current_temperature import AdminSetCurrentTemperatureRequest, AdminSetCurrentTemperatureResponse


class AdminSetCurrentTemperatureServiceImpl(AdminSetCurrentTemperatureService):
    def __init__(self, inj):
        self.master_air_cond = inj.require(MasterAirCond)  # type: MasterAirCond

    def serve(self, req: AdminSetCurrentTemperatureRequest) -> AdminSetCurrentTemperatureResponse or FailedResponse:
        self.master_air_cond.current_temperature = req.target
        return AdminSetCurrentTemperatureResponse()
