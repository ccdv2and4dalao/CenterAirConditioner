from flask import Flask
from flask_cors import CORS

import lib.functional
from abstract.component import ConfigurationProvider, OptionProvider, Logger, MasterAirCond, SystemEntropyProvider, \
    UUIDGenerator, Dispatcher, ConnectionPool
# abstract layer
from abstract.component.fan_pipe import MasterFanPipe
from abstract.component.jwt import JWT
from abstract.component.password_verifier import PasswordVerifier
from abstract.component.websocket_conn import WebsocketConn
from abstract.controller import PingController, ConnectController, AdminController, MetricsController, \
    StatisticsController, SlaveStateControlController
from abstract.database import SQLDatabase
from abstract.middleware.auth import AuthAdminMiddleware, AuthSlaveMiddleware
from abstract.model import UserInRoomRelationshipModel, UserModel, RoomModel, MetricModel, StatisticModel, \
    ReportModel, EventModel, Room
from abstract.service import ConnectionService, StartStateControlService, StopStateControlService, MetricsService, \
    GenerateStatisticService, DisConnectionService
from abstract.service.admin import AdminSetModeService, AdminSetCurrentTemperatureService, \
    AdminGetSlaveStatisticsService, AdminGetServerStatusService, AdminGetConnectedSlavesService, \
    AdminGenerateReportService, AdminBootMasterService, AdminBootMasterDaemonService, AdminShutdownMasterService, AdminShutdownMasterDaemonService, AdminGetConnectedSlaveService, \
    AdminSetUpdateDelayService, AdminSetMetricDelayService, AdminLoginService
from abstract.singleton import register_singletons
from app.component import QueueDispatcherWithThreadPool, MasterAirCondImpl
from app.component.fan_pipe import MasterFanPipeImpl
from app.config import APPVersion, APPDescription, APPName
from app.controller import PingControllerFlaskImpl, ConnectControllerFlaskImpl
from app.controller.admin import AdminControllerFlaskImpl
from app.controller.metrics import MetricsControllerFlaskImpl
from app.controller.slave_state_control import SlaveStateControlControllerFlaskImpl
from app.controller.statistics import StatisticsControllerFlaskImpl
# implementations
from app.database import BaseSQLDatabaseImpl
from app.middleware.auth import AuthAdminMiddlewareImpl, AuthSlaveMiddlewareImpl
from app.model import UserModelImpl, RoomModelImpl, UserInRoomRelationshipModelImpl, MetricsModelImpl, \
    StatisticModelImpl, ReportModelImpl, EventModelImpl
from app.router.flask import MasterFlaskRouter, FlaskRouteController, RouteController
from app.service.admin import AdminGenerateReportServiceImpl, AdminSetUpdateDelayServiceImpl, \
    AdminSetMetricDelayServiceImpl
from app.service.admin.boot import AdminBootMasterServiceImpl, AdminBootMasterDaemonServiceImpl
from app.service.admin.login import AdminLoginServiceImpl
from app.service.admin.get_connected_slaves import AdminGetConnectedSlavesServiceImpl, AdminGetConnectedSlaveServiceImpl
from app.service.admin.get_server_status import AdminGetServerStatusServiceImpl
from app.service.admin.get_slave_statistics import AdminGetSlaveStatisticsServiceImpl
from app.service.admin.set_current_temperature import AdminSetCurrentTemperatureServiceImpl
from app.service.admin.set_mode import AdminSetModeServiceImpl
from app.service.admin.shutdown import AdminShutdownMasterServiceImpl, AdminShutdownMasterDaemonServiceImpl
from app.service.connect import ConnectionServiceImpl
from app.service.generate_statistics import GenerateStatisticServiceImpl
from app.service.metrics import MetricsServiceImpl
from app.service.start_state_control import StartStateControlServiceImpl
from app.service.stop_state_control import StopStateControlServiceImpl
from app.service.disconnect import DisConnectionServiceImpl
# external dependencies
from lib import std_logging
from lib.arg_parser import StdArgParser
from lib.bcrypt_password_verifier import BCryptPasswordVerifier
from lib.file_configuration import FileConfigurationProvider
from lib.injector import Injector
from lib.memory_connection_pool import SafeMemoryConnectionPoolImpl
from lib.py_jwt import PyJWTImpl
from lib.serializer import JSONSerializer, Serializer
from lib.socket_io import functional_flask_socket_io_connection_impl
from lib.sql_sqlite3 import SQLite3
from lib.system_entropy_provider import SystemEntropyProviderImpl
from lib.system_entropy_uuid import SystemEntropyUUIDGeneratorImpl


class ServerBuilderConfiguration:
    def __init__(self):
        self.use_test_database = False


# noinspection PyMethodMayBeStatic
class ServerBuilder:
    def __init__(self, inj: Injector = None, cfg: ServerBuilderConfiguration = None, use_test_database: bool = None):
        self.injector = inj or Injector()
        self.cfg = cfg or ServerBuilderConfiguration()
        if use_test_database is not None:
            self.cfg.use_test_database = use_test_database
        self.logger = None
        self.db_conn = None

    def build(self):
        """
        Injector中保存了构建的上下文
        injector的使用方法参考 lib/injector.py类的说明
        """
        lib.functional.compose_(*[
            # 分层构建模块
            self.build_base,
            self.build_model,
            self.build_middleware,
            self.build_service,
            self.build_controller,

            # 将服务暴露到进程外
            # self.boot_server,
            # self.expose_service,
        ])(self.injector)

    def close(self):
        if self.db_conn is not None:
            del self.db_conn

    def build_base(self, inj=None):
        lib.functional.compose_(*[
            # 注入全局上下文
            self.build_global_vars,
            register_singletons,

            # 注入外部依赖
            self.build_external_dependency,
        ])(inj or self.injector)

    def build_global_vars(self, inj: Injector):
        inj.provide(APPVersion, 'v0.8.5')
        inj.provide(APPDescription, 'center air conditioner base on flask')
        inj.provide(APPName, 'center-air-conditioner-server')
        return inj

    def build_external_dependency(self, inj: Injector):
        # 无依赖接口
        inj.provide(Serializer, JSONSerializer())
        inj.build(RouteController, FlaskRouteController)

        # system接口
        inj.provide(SystemEntropyProvider, SystemEntropyProviderImpl())

        # 日志
        self.logger = std_logging.StdLoggerImpl()
        self.logger.logger.addHandler(std_logging.StreamHandler())
        inj.provide(Logger, self.logger)

        # 配置
        inj.build(OptionProvider, StdArgParser)
        inj.build(ConfigurationProvider, FileConfigurationProvider)

        # 数据库
        if self.cfg.use_test_database:
            self.db_conn = SQLite3(memory=True)
        else:
            self.db_conn = BaseSQLDatabaseImpl(inj)
        inj.provide(SQLDatabase, self.db_conn)

        inj.build(UUIDGenerator, SystemEntropyUUIDGeneratorImpl)
        inj.build(PasswordVerifier, BCryptPasswordVerifier)
        inj.build(JWT, PyJWTImpl)
        inj.provide(Flask, Flask(APPName))

        inj.provide(ConnectionPool, SafeMemoryConnectionPoolImpl())

        # todo: should provide parameters later
        # inj.build(Dispatcher, PriQueueDispatcher())
        inj.provide(Dispatcher, QueueDispatcherWithThreadPool())

        inj.provide(WebsocketConn, functional_flask_socket_io_connection_impl(inj))
        inj.build(MasterFanPipe, MasterFanPipeImpl)
        inj.build(MasterAirCond, MasterAirCondImpl)
        return inj

    # noinspection DuplicatedCode
    def build_model(self, inj: Injector = None):
        inj = inj or self.injector
        inj.build(UserModel, UserModelImpl)
        inj.build(RoomModel, RoomModelImpl)
        inj.build(UserInRoomRelationshipModel, UserInRoomRelationshipModelImpl)
        inj.build(MetricModel, MetricsModelImpl)
        inj.build(StatisticModel, StatisticModelImpl)
        inj.build(EventModel, EventModelImpl)
        inj.build(ReportModel, ReportModelImpl)
        return inj

    def create_table(self, inj: Injector = None):
        inj = inj or self.injector
        for model_prototype in [UserModel, RoomModel, UserInRoomRelationshipModel, MetricModel, StatisticModel,
                                EventModel]:
            model_instance = inj.require(model_prototype)
            created = model_instance.create()
            if not created:
                self.logger.fatal('create table failed', args={'model_type': str(model_prototype)})

    def build_middleware(self, inj: Injector = None):
        inj = inj or self.injector
        # inj.build(ReceiveRequestMiddleware, ReceiveRequestMiddlewareImpl)
        inj.build(AuthAdminMiddleware, AuthAdminMiddlewareImpl)
        inj.build(AuthSlaveMiddleware, AuthSlaveMiddlewareImpl)
        CORS(inj.require(Flask))
        return inj

    # noinspection DuplicatedCode
    def build_service(self, inj: Injector = None):
        inj = inj or self.injector
        inj.build(ConnectionService, ConnectionServiceImpl)
        inj.build(StartStateControlService, StartStateControlServiceImpl)
        inj.build(StopStateControlService, StopStateControlServiceImpl)
        inj.build(MetricsService, MetricsServiceImpl)
        inj.build(GenerateStatisticService, GenerateStatisticServiceImpl)
        inj.build(DisConnectionService, DisConnectionServiceImpl)
        inj.build(AdminGenerateReportService, AdminGenerateReportServiceImpl)
        inj.build(AdminGetConnectedSlavesService, AdminGetConnectedSlavesServiceImpl)
        inj.build(AdminGetConnectedSlaveService, AdminGetConnectedSlaveServiceImpl)
        inj.build(AdminGetServerStatusService, AdminGetServerStatusServiceImpl)
        inj.build(AdminGetSlaveStatisticsService, AdminGetSlaveStatisticsServiceImpl)
        inj.build(AdminSetCurrentTemperatureService, AdminSetCurrentTemperatureServiceImpl)
        inj.build(AdminSetModeService, AdminSetModeServiceImpl)
        inj.build(AdminLoginService, AdminLoginServiceImpl)
        inj.build(AdminBootMasterService, AdminBootMasterServiceImpl)
        inj.build(AdminShutdownMasterService, AdminShutdownMasterServiceImpl)
        inj.build(AdminBootMasterDaemonService, AdminBootMasterDaemonServiceImpl)
        inj.build(AdminShutdownMasterDaemonService, AdminShutdownMasterDaemonServiceImpl)
        inj.build(AdminSetMetricDelayService, AdminSetMetricDelayServiceImpl)
        inj.build(AdminSetUpdateDelayService, AdminSetUpdateDelayServiceImpl)
        return inj

    # noinspection DuplicatedCode
    def build_controller(self, inj: Injector = None):
        inj.build(ConnectController, ConnectControllerFlaskImpl)
        inj.build(PingController, PingControllerFlaskImpl)
        inj.build(AdminController, AdminControllerFlaskImpl)
        inj.build(MetricsController, MetricsControllerFlaskImpl)
        inj.build(StatisticsController, StatisticsControllerFlaskImpl)
        inj.build(SlaveStateControlController, SlaveStateControlControllerFlaskImpl)
        return inj

    def boot_server(self, inj: Injector = None):
        inj = inj or self.injector
        dispatcher = inj.require(Dispatcher)  # type: Dispatcher
        dispatcher.boot_up()
        self.create_table(inj)
        if self.cfg.use_test_database:
            rm = inj.require(RoomModel)  # type: RoomModel
            mm = inj.require(MetricModel)  # type: MetricModel
            em = inj.require(EventModel)  # type: EventModel
            sm = inj.require(StatisticModel)  # type: StatisticModel
            rm.insert('A-101', '1234')
            rm.insert('A-102', '1234')
            # mm.insert('A-101', '1234')
            # mm.insert('A-102', '1234')r = Room(room_id='metric_test')
            r = Room(room_id='metric_test')
            rid = rm.insert(r.room_id, r.app_key)
            r2 = Room(room_id='metric_test2')
            r2id = rid = rm.insert(r2.room_id, r2.app_key)

            em.insert_connect_event(rid)
            em.insert_start_state_control_event(rid, 'high')
            mm.insert(rid, 'high', 24.0)
            sm.insert(rid, 2.0, 10.0)
            em.insert_start_state_control_event(r2id, 'low')
            mm.insert(rid, 'high', 23.0)
            sm.insert(r2id, 1.0, 5.0)
            sm.insert(rid, 2.0, 10.0)
            mm.insert(r2id, 'low', 24.0)
            sm.insert(rid, 0.2, 1.0)
            em.insert_stop_state_control_event(rid)
            mm.insert(r2id, 'low', 23.0)
            em.insert_disconnect_event(rid)
            sm.insert(r2id, 1.0, 5.0)
            mm.insert(r2id, 'low', 22.0)
            sm.insert(r2id, 0.5, 2.5)
            em.insert_stop_state_control_event(r2id)
            em.insert_disconnect_event(r2id)
        return inj

    def expose_service(self, inj: Injector = None):
        inj = inj or self.injector
        opt = inj.require(OptionProvider)  # type: OptionProvider

        MasterFlaskRouter(inj).run(
            opt.find('host'), opt.find('port'))
