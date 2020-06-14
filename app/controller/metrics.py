from abstract.component.jwt import JWT
from abstract.controller import MetricsController
from abstract.middleware.auth import AuthSlaveMiddleware
from abstract.service import MetricsService
from app.router.flask import RouteController
from lib.injector import Injector
from proto import AuthJWTFailed
from proto.metrics import MetricsRequest


class MetricsControllerFlaskImpl(MetricsController):

    def __init__(self, inj: Injector):
        self.rc = inj.require(RouteController)  # type: RouteController
        self.auth_slave = inj.require(AuthSlaveMiddleware)  # type: AuthSlaveMiddleware
        self.s = inj.require(MetricsService)  # type: MetricsService

    def update_metrics(self, *args, **kwargs):
        req = self.rc.bind_json(MetricsRequest)  # type: MetricsRequest
        return self.auth_slave(req) or self.rc.ok(self.s.serve(req))
