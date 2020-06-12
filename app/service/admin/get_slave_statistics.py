from abstract.service.admin.get_slave_statistics import AdminGetSlaveStatisticsService
from proto import FailedResponse
from proto.admin.get_slave_statistics import AdminGetSlaveStatisticsRequest, AdminGetSlaveStatisticsResponse


class AdminGetSlaveStatisticsServiceImpl(AdminGetSlaveStatisticsService):
    def __init__(self, inj):
        pass

    def serve(self, req: AdminGetSlaveStatisticsRequest) -> AdminGetSlaveStatisticsResponse or FailedResponse:
        pass
