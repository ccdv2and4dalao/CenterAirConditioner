from abstract.service.admin import AdminGenerateReportService
from proto import FailedResponse
from proto.admin.generate_report import AdminGenerateReportRequest, AdminGenerateReportResponse
from abstract.model import ReportModel, Report
from lib.injector import Injector
import time

class AdminGenerateReportServiceImpl(AdminGenerateReportService):
    def __init__(self, inj: Injector):
        self.report_model = inj.require(ReportModel) # type: ReportModel

    def serve(self, req: AdminGenerateReportRequest) -> AdminGenerateReportResponse or FailedResponse:
        if req.stop_time == '':
            req.stop_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        reports = self.report_model.get_reports(req.stop_time, req.type)
        d = {}
        for report in reports:
            if report.room_id not in d.keys():
                d[report.room_id] = {'room_id': report.room_id, 
                                     'items': [], 
                                     'total_energy': 0.0, 
                                     'total_cost': 0.0}
            d[report.room_id]['items'].append(report)
            d[report.room_id]['total_energy'] += report.energy
            d[report.room_id]['total_cost'] += report.cost
        response = AdminGenerateReportResponse()
        response.room_list = list(d.values())
        return response