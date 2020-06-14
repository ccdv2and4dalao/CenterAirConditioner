from abstract.service.admin import AdminShutdownMasterService
from proto import FailedResponse, MasterAirCondNotAlive
from proto.admin.shutdown import AdminShutdownRequest, AdminShutdownResponse
from proto.admin.boot import AdminBootMasterRequest, AdminBootMasterResponse
from abstract.component import MasterAirCond

class AdminShutdownMasterServiceImpl(AdminShutdownMasterService):
    def __init__(self, inj):
        self.master_air_cond = inj.require(MasterAirCond)  # type: MasterAirCond

    def serve(self, req: AdminShutdownRequest) -> AdminShutdownResponse or FailedResponse:
        if not self.master_air_cond.is_boot:
            return MasterAirCondNotAlive("master aircon is off")
        self.master_air_cond.is_boot = False
        return AdminShutdownResponse()
