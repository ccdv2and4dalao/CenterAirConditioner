from abstract.consensus import ConsolePrefix
from abstract.console import SetStatisticFrequencyConsole
from app.console.base_subconsole import BaseSubConsoleImpl
from abstract.service.admin import AdminSetUpdateDelayService
from proto.admin.set_update_delay import AdminSetUpdateDelayRequest, AdminSetUpdateDelayResponse

class SetStatisticFrequencyConsoleImpl(SetStatisticFrequencyConsole, BaseSubConsoleImpl):
    def __init__(self, inj):
        super().__init__(inj)
        self.register(ConsolePrefix.set_statistic_freq)
        self.update_service = inj.require(AdminSetUpdateDelayService)

    def __call__(self, *args):
        r = AdminSetUpdateDelayRequest()
        r.delay = int(args[0])
        ret = self.update_service.serve(r)
        if type(ret) is AdminSetUpdateDelayResponse:
            print('set statistic delay success')
