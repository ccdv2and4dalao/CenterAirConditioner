from abstract.service.admin import AdminShutdownMasterService
from proto import FailedResponse
from proto.admin.shutdown import AdminShutdownRequest, AdminShutdownResponse


class AdminShutdownMasterServiceImpl(AdminShutdownMasterService):
    def __init__(self, inj):
        pass

    def serve(self, req: AdminShutdownRequest) -> AdminShutdownResponse or FailedResponse:
        print('shutdown')
        return AdminShutdownResponse()
