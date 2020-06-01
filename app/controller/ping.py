from abc import abstractmethod

from abstract.controller import PingController
from app.config import Version
from app.router.flask import RouteController
from lib.injector import Injector
from proto.ping import PingResponse


class PingControllerFlaskImpl(PingController):

    def __init__(self, inj: Injector):
        self.v = inj.require(Version)  # type: Version
        self.rc = inj.require(RouteController)  # type: RouteController

    @abstractmethod
    def ping(self, *args, **kwargs):
        return self.rc.ok(PingResponse(self.v))
