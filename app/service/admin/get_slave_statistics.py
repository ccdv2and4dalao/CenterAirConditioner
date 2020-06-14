from abstract.model import EventModel
from abstract.service.admin.get_slave_statistics import AdminGetSlaveStatisticsService
from app.service.generate_statistics import GenerateStatisticServiceImpl
from proto.admin.get_slave_statistics import AdminGetSlaveStatisticsResponse, AdminGetSlaveStatisticsRequest


class AdminGetSlaveStatisticsServiceImpl(GenerateStatisticServiceImpl, AdminGetSlaveStatisticsService):
    def __init__(self, inj):
        super().__init__(inj)
        self.response_factory = AdminGetSlaveStatisticsResponse
        self.event_model = inj.require(EventModel)

    def serve(self, req: AdminGetSlaveStatisticsRequest):
        events = self.event_model
