from abstract.controller import MetricsController
from abstract.middleware.auth import AuthSlaveMiddleware
from abstract.middleware.boot import BootMiddleware
from abstract.service import MetricsService
from app.router.flask import RouteController
from lib.injector import Injector
from proto.metrics import MetricsRequest


class MetricsControllerFlaskImpl(MetricsController):

    def __init__(self, inj: Injector):
        self.rc = inj.require(RouteController)  # type: RouteController
        self.auth_slave = inj.require(AuthSlaveMiddleware)  # type: AuthSlaveMiddleware
        self.s = inj.require(MetricsService)  # type: MetricsService
        self.check_boot = inj.require(BootMiddleware)  # type: BootMiddleware

    def update_metrics(self, *args, **kwargs):
        req = self.rc.bind_json(MetricsRequest)  # type: MetricsRequest
        return self.check_boot() or self.auth_slave(req, req.token) or self.rc.ok(self.s.serve(req))
