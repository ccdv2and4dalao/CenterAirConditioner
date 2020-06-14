from abstract.consensus import ConsolePrefix
from abstract.console import MetricConsole
from abstract.service.admin import AdminGetSlaveStatisticsService
from app.console.base_subconsole import BaseSubConsoleImpl
from proto.admin.get_slave_statistics import AdminGetSlaveStatisticsRequest


class MetricConsoleImpl(MetricConsole, BaseSubConsoleImpl):
    def __init__(self, inj):
        super().__init__(inj)
        self.register(ConsolePrefix.metric)
        self.metric_service = inj.require(AdminGetSlaveStatisticsService)

    def __call__(self, *args):
        r = AdminGetSlaveStatisticsRequest
        ret = self.metric_service.serve(r)
