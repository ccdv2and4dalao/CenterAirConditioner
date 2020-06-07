# impl example
from abstract.component import ConfigurationProvider, OptionProvider
from abstract.controller import PingController
from abstract.controller.connect import ConnectController
from abstract.service import ConnectionService
from abstract.singleton import register_singletons
from app.config import APPVersion, APPDescription
from app.controller.connect import ConnectControllerFlaskImpl
from app.controller.ping import PingControllerFlaskImpl
from app.router.flask import FlaskRouter, FlaskRouteController, RouteController
from app.service.connect import ConnectionServiceImpl
from lib.arg_parser import StdArgParser
from lib.file_configuration import FileConfigurationProvider
from lib.injector import Injector
from lib.serializer import JSONSerializer, Serializer

if __name__ == '__main__':
    injector = Injector()
    injector.provide(APPVersion, 'v0.1.0')
    injector.provide(APPDescription, 'center air conditioner base on flask')
    register_singletons(injector)
    injector.provide(Serializer, JSONSerializer())
    injector.build(OptionProvider, StdArgParser)

    injector.build(ConfigurationProvider, FileConfigurationProvider)

    injector.build(RouteController, FlaskRouteController)
    injector.build(ConnectionService, ConnectionServiceImpl)
    injector.build(ConnectController, ConnectControllerFlaskImpl)
    injector.build(PingController, PingControllerFlaskImpl)

    router = FlaskRouter(injector)
    router.run('0.0.0.0', '8080')

