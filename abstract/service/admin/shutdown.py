from abc import abstractmethod, ABC

from abstract.service import Service
from proto import FailedResponse
from proto.admin.shutdown import AdminShutdownRequest, AdminShutdownResponse


class AdminShutdownMasterService(Service, ABC):

    @abstractmethod
    def serve(self, req: AdminShutdownRequest) -> AdminShutdownResponse or FailedResponse:
        pass
