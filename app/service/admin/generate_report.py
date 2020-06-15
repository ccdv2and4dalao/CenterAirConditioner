import datetime
from dateutil.parser import parse
from abstract.model import ReportModel, EventType
from abstract.service.admin import AdminGenerateReportService
from lib.injector import Injector
from proto import FailedResponse
from proto.admin.generate_report import AdminGenerateReportRequest, AdminGenerateReportResponse

class AdminGenerateReportServiceImpl(AdminGenerateReportService):
    def __init__(self, inj: Injector):
        self.report_model = inj.require(ReportModel)  # type: ReportModel


    def serve(self, req: AdminGenerateReportRequest) -> AdminGenerateReportResponse or FailedResponse:
        if req.stop_time == '':
            req.stop_time = datetime.datetime.now()
        else:
            req.stop_time = parse(req.stop_time)
        reports, events, id2roomid = self.report_model.get_reports(req.stop_time, req.type, req.room_id)
        d = {}
        for report in reports:
            if report.room_id not in d.keys():
                d[report.room_id] = {'room_id': report.room_id,
                                     'count': 0,
                                     'items': [],
                                     'total_energy': 0.0,
                                     'total_cost': 0.0}
            d[report.room_id]['items'].append(report.__dict__)
            d[report.room_id]['total_energy'] += report.energy
            d[report.room_id]['total_cost'] += report.cost
        for event in events:
            if event.event_type == EventType.Connect:
                d[id2roomid[event.room_id]]['count'] += 1
        response = AdminGenerateReportResponse()
        response.data = list(d.values())
        return response
