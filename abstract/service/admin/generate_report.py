from abc import abstractmethod, ABC

from abstract.service import Service
from proto import FailedResponse
from proto.admin.generate_report import AdminGenerateReportRequest, AdminGenerateReportResponse

# 12.中央空调监控具备统计功能，可以根据需要给出日报表、周报表和月报表；报表内容如下：房间号、从控机开关机的次数、温控请求起止时间（列出所有记录）、温控请求的起止温度及风量消耗大小（列出所有记录）、每次温控请求所需费用、每日（周、月）所需总费用。

class AdminGenerateReportService(Service, ABC):
    @abstractmethod
    def serve(self, req: AdminGenerateReportRequest) -> AdminGenerateReportResponse or FailedResponse:
        pass