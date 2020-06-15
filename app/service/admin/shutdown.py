from abstract.service.admin import AdminShutdownMasterService, AdminShutdownMasterDaemonService
from proto import FailedResponse
from proto.admin.shutdown import AdminShutdownRequest, AdminShutdownResponse
from proto.admin.boot import AdminBootMasterRequest, AdminBootMasterResponse
from abstract.component import MasterAirCond

class AdminShutdownMasterDaemonServiceImpl(AdminShutdownMasterDaemonService):
    def __init__(self, inj):
        pass

    def serve(self, req: AdminShutdownRequest) -> AdminShutdownResponse or FailedResponse:
        return AdminShutdownResponse()


class AdminShutdownMasterServiceImpl(AdminShutdownMasterService):
    def __init__(self, inj):
        self.master_air_cond = inj.require(MasterAirCond)  # type: MasterAirCond

    def serve(self, req: AdminShutdownRequest) -> AdminShutdownResponse or FailedResponse:
        self.master_air_cond.is_boot = False
        return AdminShutdownResponse()
