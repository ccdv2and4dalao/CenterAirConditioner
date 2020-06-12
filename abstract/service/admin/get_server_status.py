from abc import abstractmethod, ABC

from abstract.service import Service
from proto import FailedResponse
from proto.admin.get_server_status import AdminGetServerStatusRequest, AdminGetServerStatusResponse


class AdminGetServerStatusService(Service, ABC):

    @abstractmethod
    def serve(self, req: AdminGetServerStatusRequest) -> AdminGetServerStatusResponse or FailedResponse:
        pass
