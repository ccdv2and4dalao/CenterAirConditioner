from abstract.service.admin import AdminGenerateReportService
from proto import FailedResponse
from proto.admin.generate_report import AdminGenerateReportRequest, AdminGenerateReportResponse
from abstract.model import ReportModel, Report, EventType
from lib.injector import Injector
import time

class AdminGenerateReportServiceImpl(AdminGenerateReportService):
    def __init__(self, inj: Injector):
        self.report_model = inj.require(ReportModel) # type: ReportModel

    def serve(self, req: AdminGenerateReportRequest) -> AdminGenerateReportResponse or FailedResponse:
        if req.stop_time == '':
            req.stop_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        reports, events, id2roomid = self.report_model.get_reports(req.stop_time, req.type)
        d = {}
        for report in reports:
            if report.room_id not in d.keys():
                d[report.room_id] = {'room_id': report.room_id, 
                                     'count': 0,
                                     'items': [], 
                                     'total_energy': 0.0, 
                                     'total_cost': 0.0,
                                     'events': []}
            d[report.room_id]['items'].append(report)
            d[report.room_id]['total_energy'] += report.energy
            d[report.room_id]['total_cost'] += report.cost
        for event in events:
            if event.event_type == EventType.Connect:
                d[id2roomid[event.room_id]]['count'] += 1
            if event.event_type == EventType.Connect or event.event_type == EventType.Disconnect:
                d[id2roomid[event.room_id]]['events'].append(event)
        response = AdminGenerateReportResponse()
        response.room_list = list(d.values())
        return response