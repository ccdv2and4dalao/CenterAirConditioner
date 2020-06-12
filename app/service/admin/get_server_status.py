from abstract.service.admin.get_server_status import AdminGetServerStatusService
from proto import FailedResponse
from proto.admin.get_server_status import AdminGetServerStatusRequest, AdminGetServerStatusResponse


class AdminGetServerStatusServiceImpl(AdminGetServerStatusService):
    def __init__(self, inj):
        pass

    def serve(self, req: AdminGetServerStatusRequest) -> AdminGetServerStatusResponse or FailedResponse:
        pass
