from abstract.component.jwt import JWT
from abstract.controller import MetricsController
from abstract.service import MetricsService
from app.router.flask import RouteController
from lib.injector import Injector
from proto import AuthJWTFailed
from proto.metrics import MetricsRequest


class MetricsControllerFlaskImpl(MetricsController):

    def __init__(self, inj: Injector):
        self.rc = inj.require(RouteController)  # type: RouteController
        self.s = inj.require(MetricsService)  # type: MetricsService
        self.jwt = inj.require(JWT)  # type: JWT

    def update_metrics(self, *args, **kwargs):
        req = self.rc.bind_json(MetricsRequest)  # type: MetricsRequest
        auth = self.jwt.authenticate(req.token)
        if isinstance(auth, Exception):
            return self.rc.err(AuthJWTFailed(f'AuthJWTFailed: {type(auth)}: {auth}'))
        req.room_id = auth['room_id']

        return self.rc.ok(self.s.serve(req))
