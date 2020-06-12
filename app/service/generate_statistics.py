from abstract.service import GenerateStatisticService
from abc import abstractmethod, ABC
from proto.generate_statistics import GenerateStatisticRequest, GenerateStatisticResponse
from lib.injector import Injector
from lib.dateutil import now
from abstract.model import EventModel, StatisticModel, Event

class BaseGenerateStatisticServiceImpl(GenerateStatisticService):
    @abstractmethod
    def get_metrics(self, room_id):
        pass


class GenerateStatisticServiceImpl(BaseGenerateStatisticServiceImpl):
    def __init__(self, inj: Injector):
        self.event_model = inj.require(EventModel)
        self.statistic_model = inj.require(StatisticModel)

    def serve(self, req: GenerateStatisticRequest):
        return self.get_metrics(req.room_id)

    def get_metrics(self, room_id):
        event = self.event_model.query_last_connect_event(room_id)
        r = GenerateStatisticResponse()
        r.energy, r.cost = self.statistic_model.query_sum_by_time_interval(room_id, event.checkpoint, now())
        return r