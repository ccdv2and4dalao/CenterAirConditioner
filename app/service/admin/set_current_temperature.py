from abstract.service.admin.set_current_temperature import AdminSetCurrentTemperatureService
from proto import FailedResponse
from proto.admin.set_current_temperature import AdminSetCurrentTemperatureRequest, AdminSetCurrentTemperatureResponse


class AdminSetCurrentTemperatureServiceImpl(AdminSetCurrentTemperatureService):
    def __init__(self, inj):
        pass

    def serve(self, req: AdminSetCurrentTemperatureRequest) -> AdminSetCurrentTemperatureResponse or FailedResponse:
        pass
