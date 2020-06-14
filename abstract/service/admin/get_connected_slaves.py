from abc import abstractmethod, ABC

from abstract.service import Service
from proto import FailedResponse
from proto.admin.get_connected_slaves import AdminGetConnectedSlavesRequest, AdminGetConnectedSlavesResponse, \
    AdminGetConnectedSlaveRequest, AdminGetConnectedSlaveResponse


class AdminGetConnectedSlavesService(Service, ABC):

    @abstractmethod
    def serve(self, req: AdminGetConnectedSlavesRequest) -> AdminGetConnectedSlavesResponse or FailedResponse:
        pass


class AdminGetConnectedSlaveService(Service, ABC):

    @abstractmethod
    def serve(self, req: AdminGetConnectedSlaveRequest) -> AdminGetConnectedSlaveResponse or FailedResponse:
        pass
