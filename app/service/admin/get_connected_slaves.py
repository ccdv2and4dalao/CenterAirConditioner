from abstract.service.admin.get_connected_slaves import AdminGetConnectedSlavesService
from proto import FailedResponse
from proto.admin.get_connected_slaves import AdminGetConnectedSlavesRequest, AdminGetConnectedSlavesResponse


class AdminGetConnectedSlavesServiceImpl(AdminGetConnectedSlavesService):

    def __init__(self, inj):
        pass

    def serve(self, req: AdminGetConnectedSlavesRequest) -> AdminGetConnectedSlavesResponse or FailedResponse:
        pass
