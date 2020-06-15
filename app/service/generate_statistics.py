from abc import abstractmethod

from abstract.model import EventModel, StatisticModel
from abstract.service import GenerateStatisticService
from lib.dateutil import now
from lib.injector import Injector
from proto.generate_statistics import GenerateStatisticRequest, GenerateStatisticResponse
from proto import MasterAirCondNotAlive
from abstract.component import MasterAirCond
from decimal import Decimal

class BaseGenerateStatisticServiceImpl(GenerateStatisticService):
    @abstractmethod
    def get_metrics(self, room_id):
        pass


class GenerateStatisticServiceImpl(BaseGenerateStatisticServiceImpl):
    def __init__(self, inj: Injector):
        self.event_model = inj.require(EventModel)
        self.statistic_model = inj.require(StatisticModel)
        self.response_factory = GenerateStatisticResponse
        self.master_air_cond = inj.require(MasterAirCond)  # type: MasterAirCond

    def serve(self, req: GenerateStatisticRequest):
        if not self.master_air_cond.is_boot:
            return MasterAirCondNotAlive("master aircon is off")
        return self.get_metrics(req.room_id)

    def get_metrics(self, room_id):
        event = self.event_model.query_last_connect_event(room_id)
        r = self.response_factory()
        r.energy, r.cost = self.statistic_model.query_sum_by_time_interval(room_id, event.checkpoint, now())
        if isinstance(r.energy, Decimal):
            r.energy, r.cost = float(r.energy), float(r.cost)
        return r
