from abc import abstractmethod, ABC

from abstract.service import Service
from proto import FailedResponse
from proto.admin.get_connected_slaves import AdminGetConnectedSlavesRequest, AdminGetConnectedSlavesResponse


class AdminGetConnectedSlavesService(Service, ABC):

    @abstractmethod
    def serve(self, req: AdminGetConnectedSlavesRequest) -> AdminGetConnectedSlavesResponse or FailedResponse:
        pass
