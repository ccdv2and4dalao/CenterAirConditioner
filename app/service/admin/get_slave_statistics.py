from abstract.service.admin.get_slave_statistics import AdminGetSlaveStatisticsService
from app.service.generate_statistics import GenerateStatisticServiceImpl
from proto.admin.get_slave_statistics import AdminGetSlaveStatisticsResponse, AdminGetSlaveStatisticsRequest
from abstract.model import EventModel, StatisticModel

class AdminGetSlaveStatisticsServiceImpl(AdminGetSlaveStatisticsService):
    def __init__(self, inj):
        super().__init__(inj)
        self.response_factory = AdminGetSlaveStatisticsResponse
        self.event_model = inj.require(EventModel)

    def serve(self, req: AdminGetSlaveStatisticsRequest):
        events = self.event_model