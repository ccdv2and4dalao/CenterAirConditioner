# impl example
from abstract.controller import PingController
from abstract.controller.connect import ConnectController
from abstract.service import ConnectionService
from app.config import Version
from app.controller.connect import ConnectControllerFlaskImpl
from app.controller.ping import PingControllerFlaskImpl
from app.router.flask import FlaskRouter, FlaskRouteController, RouteController
from app.service.connect import ConnectionServiceImpl
from lib.injector import Injector
from lib.serializer import JSONSerializer, Serializer

if __name__ == '__main__':
    injector = Injector()
    injector.provide(Version, 'v0.1.0')
    injector.provide(Serializer, JSONSerializer())

    injector.build(RouteController, FlaskRouteController)
    injector.build(ConnectionService, ConnectionServiceImpl)
    injector.build(ConnectController, ConnectControllerFlaskImpl)
    injector.build(PingController, PingControllerFlaskImpl)

    router = FlaskRouter(injector)
    router.run('127.0.0.1', '23333')

