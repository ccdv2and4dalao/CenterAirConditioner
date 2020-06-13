from abstract.console import BootConsole
from app.console.base_subconsole import BaseSubConsoleImpl
from abstract.consensus import ConsolePrefix
from abstract.service.admin import AdminBootMasterService
from proto.admin.boot import AdminBootMasterRequest

class BootConsoleImpl(BootConsole, BaseSubConsoleImpl):
    def __init__(self, inj):
        super().__init__(inj)
        self.register(ConsolePrefix.boot)
        self.boot_service = inj.require(AdminBootMasterService)

    def __call__(self, *args):
        r = AdminBootMasterRequest()
        ret = self.boot_service.serve(r)
        return ret
