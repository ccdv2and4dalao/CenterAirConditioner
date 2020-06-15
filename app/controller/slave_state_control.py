from abstract.controller import SlaveStateControlController
from abstract.middleware.auth import AuthSlaveMiddleware
from abstract.middleware.boot import BootMiddleware
from abstract.service import StartStateControlService, StopStateControlService
from app.router.flask import RouteController
from lib.injector import Injector
from proto.start_state_control import StartStateControlRequest
from proto.stop_state_control import StopStateControlRequest


class SlaveStateControlControllerFlaskImpl(SlaveStateControlController):

    def __init__(self, inj: Injector):
        self.rc = inj.require(RouteController)  # type: RouteController
        self.auth_slave = inj.require(AuthSlaveMiddleware)  # type: AuthSlaveMiddleware
        self.start_state_control_service = inj.require(StartStateControlService)  # type: StartStateControlService
        self.stop_state_control_service = inj.require(StopStateControlService)  # type: StopStateControlService
        self.check_boot = inj.require(BootMiddleware)  # type: BootMiddleware

    def start_state_control(self, *args, **kwargs):
        req = self.rc.bind_json(StartStateControlRequest)
        return self.check_boot() or self.auth_slave(req, req.token) or self.rc.ok(
            self.start_state_control_service.serve(req))

    def stop_state_control(self, *args, **kwargs):
        req = self.rc.bind_json(StopStateControlRequest)
        return self.check_boot() or self.auth_slave(req, req.token) or self.rc.ok(
            self.stop_state_control_service.serve(req))
