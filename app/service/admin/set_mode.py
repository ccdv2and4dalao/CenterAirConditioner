from abstract.service.admin.set_mode import AdminSetModeService
from proto import FailedResponse
from proto.admin.set_mode import AdminSetModeRequest, AdminSetModeResponse


class AdminSetModeServiceImpl(AdminSetModeService):
    def __init__(self, inj):
        pass

    def serve(self, req: AdminSetModeRequest) -> AdminSetModeResponse or FailedResponse:
        pass
