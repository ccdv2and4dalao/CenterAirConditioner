from abstract.service.admin import AdminBootMasterService, AdminBootMasterDaemonService
from proto import FailedResponse
from proto.admin.boot import AdminBootMasterRequest, AdminBootMasterResponse
from abstract.component import MasterAirCond

class AdminBootMasterDaemonServiceImpl(AdminBootMasterDaemonService):
    def __init__(self, inj):
        pass

    def serve(self, req: AdminBootMasterRequest) -> AdminBootMasterResponse or FailedResponse:
        return AdminBootMasterResponse()

class AdminBootMasterServiceImpl(AdminBootMasterService):
    def __init__(self, inj):
        self.master_air_cond = inj.require(MasterAirCond)  # type: MasterAirCond

    def serve(self, req: AdminBootMasterRequest) -> AdminBootMasterResponse or FailedResponse:
        if not self.master_air_cond.is_boot:
            self.master_air_cond.is_boot = True
        return AdminBootMasterResponse()
