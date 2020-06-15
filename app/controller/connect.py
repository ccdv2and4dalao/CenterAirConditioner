from abstract.controller.connect import ConnectController
from abstract.service import ConnectionService, DisConnectionService
from app.router.flask import RouteController
from lib.injector import Injector
from proto.connection import ConnectionRequest
from proto.disconnect import DisConnectionRequest
from abstract.middleware.auth import AuthSlaveMiddleware

class ConnectControllerFlaskImpl(ConnectController):

    def __init__(self, inj: Injector):
        self.rc = inj.require(RouteController)  # type: RouteController
        self.s = inj.require(ConnectionService)  # type: ConnectionService
        self.dc = inj.require(DisConnectionService) # type: DisConnectionService
        self.auth = inj.require(AuthSlaveMiddleware) # type: AuthSlaveMiddleware

    def connect(self, *args, **kwargs):
        return self.rc.ok(self.s.serve(self.rc.bind_json(ConnectionRequest)))

    def disconnect(self, *args, **kwargs):
        req = self.rc.bind_json(DisConnectionRequest) # type: DisConnectionRequest
        return self.auth_slave(req, req.token) or self.rc.ok(self.s.serve(req))
