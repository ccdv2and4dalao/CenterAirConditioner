# impl example

import lib.functional
from abstract.component import ConfigurationProvider, OptionProvider, Logger, MasterAirCond
from abstract.controller import PingController
from abstract.controller.connect import ConnectController
from abstract.model import UserInRoomRelationshipModel, UserModel, RoomModel
from abstract.service import ConnectionService
from abstract.singleton import register_singletons
from app.component.air import MasterAirCondImpl
from app.config import APPVersion, APPDescription
from app.controller.connect import ConnectControllerFlaskImpl
from app.controller.ping import PingControllerFlaskImpl
from app.router.flask import FlaskRouter, FlaskRouteController, RouteController
from app.service.connect import ConnectionServiceImpl
from lib import std_logging
from lib.arg_parser import StdArgParser
from lib.file_configuration import FileConfigurationProvider
from lib.injector import Injector
from lib.serializer import JSONSerializer, Serializer
from mock.model import MockUserModel, MockRoomModel, MockUserInRoomRelationshipModel


def inject_global_vars(inj: Injector):
    inj.provide(APPVersion, 'v0.1.0')
    inj.provide(APPDescription, 'center air conditioner base on flask')
    return inj


def inject_external_dependency(inj: Injector):
    inj.provide(Serializer, JSONSerializer())

    logger = std_logging.StdLoggerImpl()
    logger.logger.addHandler(std_logging.StreamHandler())
    inj.provide(Logger, logger)

    inj.build(OptionProvider, StdArgParser)
    inj.build(ConfigurationProvider, FileConfigurationProvider)
    inj.build(MasterAirCond, MasterAirCondImpl)
    return inj


def inject_model(inj: Injector):
    inj.provide(UserModel, MockUserModel())
    inj.provide(RoomModel, MockRoomModel())
    inj.provide(UserInRoomRelationshipModel, MockUserInRoomRelationshipModel())
    return inj


def inject_service(inj: Injector):
    inj.build(ConnectionService, ConnectionServiceImpl)
    return inj


def inject_controller(inj: Injector):
    inj.build(RouteController, FlaskRouteController)
    inj.build(ConnectController, ConnectControllerFlaskImpl)
    inj.build(PingController, PingControllerFlaskImpl)
    return inj


def expose_service(inj: Injector):
    opt = inj.require(OptionProvider)  # type: OptionProvider

    FlaskRouter(inj).run(
        opt.find('host'), opt.find('port'))


if __name__ == '__main__':
    """
    Injector中保存了构建的上下文
    injector的使用方法参考 lib/injector.py类的说明
    """
    lib.functional.compose_(*[

        # 注入全局上下文
        inject_global_vars,
        register_singletons,

        # 注入外部依赖
        inject_external_dependency,

        # 分层构建模块
        inject_model,
        inject_service,
        inject_controller,

        # 将服务暴露到进程外
        expose_service,
    ])(Injector())  # type: Injector
