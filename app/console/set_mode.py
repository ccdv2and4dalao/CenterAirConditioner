from abstract.console import SetModeConsole
from app.console.base_subconsole import BaseSubConsoleImpl
from abstract.consensus import ConsolePrefix
from abstract.service.admin import AdminSetModeService
from proto.admin.set_mode import AdminSetModeRequest, AdminSetModeResponse

class SetModeConsoleImpl(SetModeConsole, BaseSubConsoleImpl):
    def __init__(self, inj):
        super().__init__(inj)
        self.register(ConsolePrefix.set_mode)
        self.set_mode_service = inj.require(AdminSetModeService)

    def __call__(self, *args):
        r = AdminSetModeRequest()
        r.mode = args[0]
        ret = self.set_mode_service.serve(r)
        if type(ret) is AdminSetModeResponse:
            print('set mode success')