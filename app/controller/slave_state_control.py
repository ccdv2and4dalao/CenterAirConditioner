from abstract.controller import SlaveStateControlController
from abstract.service import StartStateControlService, StopStateControlService
from app.router.flask import RouteController
from lib.injector import Injector
from proto.start_state_control import StartStateControlRequest
from proto.stop_state_control import StopStateControlRequest


class SlaveStateControlControllerFlaskImpl(SlaveStateControlController):

    def __init__(self, inj: Injector):
        self.rc = inj.require(RouteController)  # type: RouteController
        self.start_state_control_service = inj.require(StartStateControlService)  # type: StartStateControlService
        self.stop_state_control_service = inj.require(StopStateControlService)  # type: StopStateControlService

    def start_state_control(self, *args, **kwargs):
        return self.rc.ok(self.start_state_control_service.serve(self.rc.bind_json(StartStateControlRequest)))

    def stop_state_control(self, *args, **kwargs):
        return self.rc.ok(self.stop_state_control_service.serve(self.rc.bind_json(StopStateControlRequest)))
