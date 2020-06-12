from abc import abstractmethod, ABC

from abstract.service import Service
from proto import FailedResponse
from proto.admin.get_slave_statistics import AdminGetSlaveStatisticsRequest, AdminGetSlaveStatisticsResponse


class AdminGetSlaveStatisticsService(Service, ABC):

    @abstractmethod
    def serve(self, req: AdminGetSlaveStatisticsRequest) -> AdminGetSlaveStatisticsResponse or FailedResponse:
        pass
