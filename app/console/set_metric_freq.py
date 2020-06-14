from abstract.consensus import ConsolePrefix
from abstract.console import SetMetricFrequencyConsole
from app.console.base_subconsole import BaseSubConsoleImpl
from abstract.service.admin import AdminSetMetricDelayService
from proto.admin.set_metric_delay import AdminSetMetricDelayRequest, AdminSetMetricDelayResponse


class SetMetricFrequencyConsoleImpl(SetMetricFrequencyConsole, BaseSubConsoleImpl):
    def __init__(self, inj):
        super().__init__(inj)
        self.register(ConsolePrefix.set_metric_freq)
        self.set_metric_service = inj.require(AdminSetMetricDelayService)

    def __call__(self, *args):
        r = AdminSetMetricDelayRequest()
        r.delay = int(args[0])
        ret = self.set_metric_service.serve(r)
        if type(ret) is AdminSetMetricDelayResponse:
            print('set metric delay success')
