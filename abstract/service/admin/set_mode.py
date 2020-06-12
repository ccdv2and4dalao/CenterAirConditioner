from abc import abstractmethod, ABC

from abstract.service import Service
from proto import FailedResponse
from proto.admin.set_mode import AdminSetModeRequest, AdminSetModeResponse


class AdminSetModeService(Service, ABC):

    @abstractmethod
    def serve(self, req: AdminSetModeRequest) -> AdminSetModeResponse or FailedResponse:
        pass
