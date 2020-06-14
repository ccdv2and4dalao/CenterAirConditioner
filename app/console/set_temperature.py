from abstract.consensus import ConsolePrefix
from abstract.console import SetTemperatureConsole
from abstract.service.admin import AdminSetCurrentTemperatureService
from app.console.base_subconsole import BaseSubConsoleImpl
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
