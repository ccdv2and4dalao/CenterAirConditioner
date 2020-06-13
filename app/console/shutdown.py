from abstract.console import ShutdownConsole
from app.console.base_subconsole import BaseSubConsoleImpl
from abstract.consensus import ConsolePrefix
from abstract.service.admin import AdminShutdownMasterService
from proto.admin.shutdown import AdminShutdownRequest, AdminShutdownResponse

class ShutdownConsoleImpl(ShutdownConsole, BaseSubConsoleImpl):
    def __init__(self, inj):
        super().__init__(inj)
        self.register(ConsolePrefix.shutdown)
        self.shutdown_service = inj.require(AdminShutdownMasterService)

    def __call__(self, *args):
        r = AdminShutdownRequest()
        ret = self.shutdown_service.serve(r)
        if type(ret) is AdminShutdownResponse:
            print('shutdown success')
