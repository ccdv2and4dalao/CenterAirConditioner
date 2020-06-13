from abstract.service.admin.get_slave_statistics import AdminGetSlaveStatisticsService
from app.service.generate_statistics import GenerateStatisticServiceImpl
from proto.admin.get_slave_statistics import AdminGetSlaveStatisticsResponse


class AdminGetSlaveStatisticsServiceImpl(GenerateStatisticServiceImpl, AdminGetSlaveStatisticsService):
    def __init__(self, inj):
        super().__init__(inj)
        self.response_factory = AdminGetSlaveStatisticsResponse
