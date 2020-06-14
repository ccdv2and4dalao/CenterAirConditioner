from abc import abstractmethod, ABC

from abstract.service import Service
from proto import FailedResponse
from proto.admin.boot import AdminBootMasterRequest, AdminBootMasterResponse


class AdminBootMasterService(Service, ABC):

    @abstractmethod
    def serve(self, req: AdminBootMasterRequest) -> AdminBootMasterResponse or FailedResponse:
        pass


class AdminBootMasterDaemonService(Service, ABC):

    @abstractmethod
    def serve(self, req: AdminBootMasterRequest) -> AdminBootMasterResponse or FailedResponse:
        pass
