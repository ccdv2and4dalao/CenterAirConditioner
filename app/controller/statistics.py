from abstract.controller import StatisticsController
from abstract.middleware.auth import AuthSlaveMiddleware
from abstract.middleware.boot import BootMiddleware
from abstract.service import GenerateStatisticService
from app.router.flask import RouteController
from lib.injector import Injector
from proto.generate_statistics import GenerateStatisticRequest


class StatisticsControllerFlaskImpl(StatisticsController):

    def __init__(self, inj: Injector):
        self.rc = inj.require(RouteController)  # type: RouteController
        self.auth_slave = inj.require(AuthSlaveMiddleware)  # type: AuthSlaveMiddleware
        self.s = inj.require(GenerateStatisticService)  # type: GenerateStatisticService
        self.check_boot = inj.require(BootMiddleware)  # type: BootMiddleware

    def generate_statistics(self, *args, **kwargs):
        req = self.rc.bind(GenerateStatisticRequest)
        return self.check_boot() or self.auth_slave(req, req.token) or self.rc.ok(self.s.serve(req))
