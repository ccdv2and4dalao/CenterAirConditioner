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
        d = {'room_id': id2roomid[int(req.room_id)],
            'count': 0,
            'items': [],
            'total_energy': 0.0,
            'total_cost': 0.0}
        for report in reports:
            d['items'].append(report.__dict__)
            d['total_energy'] += report.energy
            d['total_cost'] += report.cost
        for event in events:
            if event.event_type == EventType.Connect:
                d['count'] += 1
        response = AdminGenerateReportResponse()
        response.data = d
        return response
