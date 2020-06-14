from abstract.consensus import ConsolePrefix
from abstract.console import MetricConsole
from abstract.service.admin import AdminGetSlaveStatisticsService
from app.console.base_subconsole import BaseSubConsoleImpl
from proto.admin.get_slave_statistics import AdminGetSlaveStatisticsRequest
from prettytable import PrettyTable

class MetricConsoleImpl(MetricConsole, BaseSubConsoleImpl):
    def __init__(self, inj):
        super().__init__(inj)
        self.register(ConsolePrefix.metric)
        self.metric_service = inj.require(AdminGetSlaveStatisticsService)

    def __call__(self, *args):
        r = AdminGetSlaveStatisticsRequest
        ret = self.metric_service.serve(r)
        attrs = ['room_id', 'start_time', 'stop_time', 'fan_speed', 'energy', 'cost']
        table = PrettyTable(attrs)
        for d in ret.data:
            table.add_row([d[attr] for attr in attrs])
        print(table)
