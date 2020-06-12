from abc import abstractmethod, ABC

from abstract.service import Service
from proto import FailedResponse
from proto.admin.set_current_temperature import AdminSetCurrentTemperatureRequest, AdminSetCurrentTemperatureResponse


class AdminSetCurrentTemperatureService(Service, ABC):

    @abstractmethod
    def serve(self, req: AdminSetCurrentTemperatureRequest) -> AdminSetCurrentTemperatureResponse or FailedResponse:
        pass
