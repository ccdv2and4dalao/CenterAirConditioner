from abstract.console import SetTemperatureConsole
from app.console.base_subconsole import BaseSubConsoleImpl
from abstract.consensus import ConsolePrefix
from abstract.service.admin import AdminSetCurrentTemperatureService
from proto.admin.set_current_temperature import AdminSetCurrentTemperatureRequest, AdminSetCurrentTemperatureResponse

class SetTemperatureConsoleImpl(SetTemperatureConsole, BaseSubConsoleImpl):
    def __init__(self, inj):
        super().__init__(inj)
        self.register(ConsolePrefix.set_temperature)
        self.temperature_service = inj.require(AdminSetCurrentTemperatureService)

    def __call__(self, *args):
        r = AdminSetCurrentTemperatureRequest()
        ret = self.temperature_service.serve(r)
        if type(ret) is AdminSetCurrentTemperatureResponse:
            print('set temperature success')
