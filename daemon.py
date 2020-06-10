import lib.functional
from abstract.component import OptionProvider, Logger
from abstract.controller import PingController, DaemonAdminController
from abstract.singleton import register_singletons
from app.config import APPVersion, APPDescription
from app.controller.admin import FlaskDaemonAdminControllerImpl
from app.controller.ping import PingControllerFlaskImpl
from app.router.flask import DaemonFlaskRouter, FlaskRouteController, RouteController
from lib import std_logging
from lib.arg_parser import StdArgParser
from lib.injector import Injector
from lib.serializer import JSONSerializer, Serializer


def inject_global_vars(inj: Injector):
    inj.provide(APPVersion, 'v0.1.0')
    inj.provide(APPDescription, 'center air conditioner daemon base on flask')
    return inj


def inject_external_dependency(inj: Injector):
    # 无依赖接口
    inj.provide(Serializer, JSONSerializer())

    # 日志
    logger = std_logging.StdLoggerImpl()
    logger.logger.addHandler(std_logging.StreamHandler())
    inj.provide(Logger, logger)

    inj.build(OptionProvider, StdArgParser)
    return inj


def inject_middleware(inj: Injector):
    return inj


def inject_service(inj: Injector):
    return inj


def inject_controller(inj: Injector):
    inj.build(RouteController, FlaskRouteController)
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
