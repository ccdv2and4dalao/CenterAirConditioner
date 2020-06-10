from abc import abstractmethod, ABC

from abstract.service import Service
from proto import FailedResponse
from proto.admin.generate_report import AdminGenerateReportRequest, AdminGenerateReportResponse

class AdminGenerateReportService(Service, ABC):
    @abstractmethod
    def serve(self, req: AdminGenerateReportRequest) -> AdminGenerateReportResponse or FailedResponse:
        pass