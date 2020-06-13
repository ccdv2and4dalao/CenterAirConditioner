from abstract.controller import StatisticsController
from abstract.service import GenerateStatisticService
from app.router.flask import RouteController
from lib.injector import Injector
from proto.generate_statistics import GenerateStatisticRequest


class StatisticsControllerFlaskImpl(StatisticsController):

    def __init__(self, inj: Injector):
        self.rc = inj.require(RouteController)  # type: RouteController
        self.s = inj.require(GenerateStatisticService)  # type: GenerateStatisticService

    def generate_statistics(self, *args, **kwargs):
        return self.rc.ok(self.s.serve(self.rc.bind_json(GenerateStatisticRequest)))
