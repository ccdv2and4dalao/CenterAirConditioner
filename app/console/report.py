from prettytable import PrettyTable

from abstract.consensus import ConsolePrefix
from abstract.console import ReportConsole
from abstract.model import Report
from abstract.service.admin import AdminGenerateReportService
from app.console.base_subconsole import BaseSubConsoleImpl
from proto.admin.generate_report import AdminGenerateReportRequest, AdminGenerateReportResponse


class ReportConsoleImpl(ReportConsole, BaseSubConsoleImpl):
    def __init__(self, inj):
        super().__init__(inj)
        self.register(ConsolePrefix.report)
        self.report_service = inj.require(AdminGenerateReportService)

    def __call__(self, *args):
        duration = args[0].lower()
        room_id = args[1] if len(args) == 2 else None
        if duration not in ['day', 'week', 'month']:
            raise ValueError('report type should in [day, week, month]')
        r = AdminGenerateReportRequest()
        r.type = duration
        r.room_id = room_id
        ret = self.report_service.serve(r)

        if type(ret) is AdminGenerateReportResponse:
            d = ret.data
            print(
                f"room: {d['room_id']}\ttotal energy: {d['total_energy']}\t total cost: {d['total_cost']}\t total boots: {d['count']}")
            print('details:')
            table = PrettyTable([Report.start_time_key, Report.stop_time_key,
                                 Report.start_temperature_key, Report.end_temperature_key,
                                 Report.energy_key, Report.cost_key])
            for report in d['items']:
                table.add_row([report['start_time'], report['stop_time'],
                               report['start_temperature'], report['end_temperature'],
                               report['energy'], report['cost']])
            print(table)
            print('')
