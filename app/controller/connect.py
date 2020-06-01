from abc import abstractmethod

from abstract.controller.connect import ConnectController
from abstract.service import ConnectionService, ConnectionRequest
from app.router.flask import RouteController
from lib.injector import Injector


class ConnectControllerFlaskImpl(ConnectController):

    def __init__(self, inj: Injector):
        self.rc = inj.require(RouteController)  # type: RouteController
        self.s = inj.require(ConnectionService)  # type: ConnectionService

    @abstractmethod
    def connect(self, *args, **kwargs):
        return self.rc.ok(self.s.serve(self.rc.bind_json(ConnectionRequest)))
