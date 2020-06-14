from flask import Flask
from flask_cors import CORS

import lib.functional
from abstract.component import OptionProvider, Logger, ConfigurationProvider, SystemEntropyProvider
from abstract.component.jwt import JWT
from abstract.controller import PingController, DaemonAdminController
from abstract.middleware.auth import AuthAdminMiddleware
from abstract.service.admin import AdminLoginService, AdminBootMasterService, AdminShutdownMasterService
from abstract.singleton import register_singletons
from app.config import APPVersion, APPDescription, APPName
from app.controller.admin import FlaskDaemonAdminControllerImpl
from app.controller.ping import PingControllerFlaskImpl
from app.middleware.auth import AuthAdminMiddlewareImpl
from app.router.flask import DaemonFlaskRouter, FlaskRouteController, RouteController
from app.service.admin import AdminLoginServiceImpl, AdminBootMasterServiceImpl, AdminShutdownMasterServiceImpl
from lib import std_logging
from lib.arg_parser import StdArgParser
from lib.file_configuration import FileConfigurationProvider
from lib.injector import Injector
from lib.py_jwt import PyJWTImpl
from lib.serializer import JSONSerializer, Serializer
from lib.system_entropy_provider import SystemEntropyProviderImpl


def inject_global_vars(inj: Injector):
    inj.provide(APPVersion, 'v0.1.0')
    inj.provide(APPDescription, 'center air conditioner daemon base on flask')
    inj.provide(APPName, 'center-air-conditioner-daemon')
    return inj


def inject_external_dependency(inj: Injector):
    # 无依赖接口
    inj.provide(Serializer, JSONSerializer())

    # system接口
    inj.provide(SystemEntropyProvider, SystemEntropyProviderImpl())

    # 日志
    logger = std_logging.StdLoggerImpl()
    logger.logger.addHandler(std_logging.StreamHandler())
    inj.provide(Logger, logger)
    inj.provide(Flask, Flask(APPName))

    inj.build(OptionProvider, StdArgParser)
    inj.build(ConfigurationProvider, FileConfigurationProvider)
    inj.build(RouteController, FlaskRouteController)
    inj.build(JWT, PyJWTImpl)

    return inj


def inject_middleware(inj: Injector):
    inj.build(AuthAdminMiddleware, AuthAdminMiddlewareImpl)
    CORS(inj.require(Flask))
    return inj


def inject_service(inj: Injector):
    inj.build(AdminLoginService, AdminLoginServiceImpl)
    inj.build(AdminBootMasterService, AdminBootMasterServiceImpl)
    inj.build(AdminShutdownMasterService, AdminShutdownMasterServiceImpl)

    return inj


def inject_controller(inj: Injector):
    inj.build(PingController, PingControllerFlaskImpl)
    inj.build(DaemonAdminController, FlaskDaemonAdminControllerImpl)
    return inj


def boot_server(inj: Injector):
    return inj


def expose_service(inj: Injector):
    opt = inj.require(OptionProvider)  # type: OptionProvider

    DaemonFlaskRouter(inj).run(
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
        inject_middleware,
        inject_service,
        inject_controller,

        # 将服务暴露到进程外
        boot_server,
        expose_service,
    ])(Injector())  # type: Injector
