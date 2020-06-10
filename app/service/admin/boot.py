from abstract.service.admin import AdminBootMasterService
from proto import FailedResponse
from proto.admin.boot import AdminBootMasterRequest, AdminBootMasterResponse


class AdminBootMasterServiceImpl(AdminBootMasterService):
    def __init__(self, inj):
        pass

    def serve(self, req: AdminBootMasterRequest) -> AdminBootMasterResponse or FailedResponse:
        print('boot')
        return AdminBootMasterResponse()
