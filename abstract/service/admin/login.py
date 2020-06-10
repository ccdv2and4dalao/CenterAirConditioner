from abc import abstractmethod, ABC

from abstract.service import Service
from proto import FailedResponse
from proto.admin.login import AdminLoginRequest, AdminLoginResponse


class AdminLoginService(Service, ABC):

    @abstractmethod
    def serve(self, req: AdminLoginRequest) -> AdminLoginResponse or FailedResponse:
        pass
