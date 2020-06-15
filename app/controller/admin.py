from abstract.controller import AdminController, DaemonAdminController
from abstract.middleware.auth import AuthAdminMiddleware
from abstract.middleware.boot import BootMiddleware
from abstract.service.admin import AdminLoginService, AdminGenerateReportService, \
    AdminGetConnectedSlavesService, AdminGetServerStatusService, AdminGetSlaveStatisticsService, \
    AdminSetCurrentTemperatureService, AdminSetModeService, AdminBootMasterService, AdminBootMasterDaemonService, \
    AdminShutdownMasterService, AdminShutdownMasterDaemonService
from abstract.service.admin.get_connected_slaves import AdminGetConnectedSlaveService
from abstract.service.admin.get_room_count import AdminGetRoomCountService
from abstract.service.admin.set_metric_delay import AdminSetMetricDelayService
from abstract.service.admin.set_update_delay import AdminSetUpdateDelayService
from app.router.flask import RouteController
from lib.injector import Injector
# transport layer objects
from proto.admin.boot import AdminBootMasterRequest
from proto.admin.generate_report import AdminGenerateReportRequest
from proto.admin.get_connected_slaves import AdminGetConnectedSlavesRequest, AdminGetConnectedSlaveRequest
from proto.admin.get_room_count import AdminGetRoomCountRequest
from proto.admin.get_server_status import AdminGetServerStatusRequest
from proto.admin.get_slave_statistics import AdminGetSlaveStatisticsRequest
from proto.admin.login import AdminLoginRequest
from proto.admin.set_current_temperature import AdminSetCurrentTemperatureRequest
from proto.admin.set_mode import AdminSetModeRequest
from proto.admin.shutdown import AdminShutdownRequest
from proto.admin.set_metric_delay import AdminSetMetricDelayRequest
from proto.admin.set_update_delay import AdminSetUpdateDelayRequest


class FlaskDaemonAdminControllerImpl(DaemonAdminController):

    def __init__(self, inj: Injector):
        self.rc = inj.require(RouteController)  # type: RouteController
        self.master_is_boot = inj.require(BootMiddleware)
        self.auth_admin = inj.require(AuthAdminMiddleware)  # type: AuthAdminMiddleware
        self.login_service = inj.require(AdminLoginService)
        self.boot_service = inj.require(AdminBootMasterDaemonService)
        self.shutdown_service = inj.require(AdminShutdownMasterDaemonService)

    def login(self, *args, **kwargs):
        return self.rc.ok(self.login_service.serve(self.rc.bind(AdminLoginRequest)))

    def boot(self, *args, **kwargs):
        req = self.rc.bind(AdminBootMasterRequest)  # type: AdminBootMasterRequest
        return self.auth_admin(req.jwt_token) or self.rc.ok(self.boot_service.serve(req))

    def shutdown(self, *args, **kwargs):
        req = self.rc.bind(AdminShutdownRequest)  # type: AdminShutdownRequest
        return self.auth_admin(req.jwt_token) or self.rc.ok(self.shutdown_service.serve(req))


class AdminControllerFlaskImpl(AdminController):

    def __init__(self, inj: Injector):
        self.rc = inj.require(RouteController)  # type: RouteController
        self.master_is_boot = inj.require(BootMiddleware)
        self.auth_admin = inj.require(AuthAdminMiddleware)  # type: AuthAdminMiddleware
        self.generate_report_service = inj.require(AdminGenerateReportService)  # type: AdminGenerateReportService
        self.get_connected_slaves_service = inj.require(
            AdminGetConnectedSlavesService)  # type: AdminGetConnectedSlavesService
        self.get_connected_slave_service = inj.require(
            AdminGetConnectedSlaveService)  # type: AdminGetConnectedSlaveService
        self.get_server_status_service = inj.require(AdminGetServerStatusService)  # type: AdminGetServerStatusService
        self.get_slave_statistics_service = inj.require(
            AdminGetSlaveStatisticsService)  # type: AdminGetSlaveStatisticsService
        self.set_current_temperature_service = inj.require(
            AdminSetCurrentTemperatureService)  # type: AdminSetCurrentTemperatureService
        self.set_mode_service = inj.require(AdminSetModeService)  # type: AdminSetModeService
        self.admin_login_service = inj.require(AdminLoginService)
        self.admin_boot_master_service = inj.require(AdminBootMasterService)
        self.admin_shutdown_master_service = inj.require(AdminShutdownMasterService)
        self.get_room_count_service = inj.require(AdminGetRoomCountService)
        self.set_metrics_delay_service = inj.require(AdminSetMetricDelayService)
        self.set_update_delay_service = inj.require(AdminSetUpdateDelayService)

    def set_mode(self, *args, **kwargs):
        req = self.rc.bind(AdminSetModeRequest)  # type: AdminSetModeRequest
        return self.master_is_boot() or self.auth_admin(req.jwt_token) or self.rc.ok(self.set_mode_service.serve(req))

    def set_current_temperature(self, *args, **kwargs):
        req = self.rc.bind(AdminSetCurrentTemperatureRequest)  # type: AdminSetCurrentTemperatureRequest
        return self.master_is_boot() or self.auth_admin(req.jwt_token) or self.rc.ok(self.set_current_temperature_service.serve(req))

    def get_server_status(self, *args, **kwargs):
        req = self.rc.bind(AdminGetServerStatusRequest)  # type: AdminGetServerStatusRequest
        return self.auth_admin(req.jwt_token) or self.rc.ok(self.get_server_status_service.serve(req))

    def get_slave_statistics(self, *args, **kwargs):
        req = self.rc.bind(AdminGetSlaveStatisticsRequest)  # type: AdminGetSlaveStatisticsRequest
        return self.master_is_boot() or self.auth_admin(req.jwt_token) or self.rc.ok(self.get_slave_statistics_service.serve(req))

    def get_report(self, *args, **kwargs):
        req = self.rc.bind(AdminGenerateReportRequest)  # type: AdminGenerateReportRequest
        return self.master_is_boot() or self.auth_admin(req.jwt_token) or self.rc.ok(self.generate_report_service.serve(req))

    def get_connected_slaves(self, *args, **kwargs):
        req = self.rc.bind(AdminGetConnectedSlavesRequest)  # type: AdminGetConnectedSlavesRequest
        return self.master_is_boot() or self.auth_admin(req.jwt_token) or self.rc.ok(self.get_connected_slaves_service.serve(req))

    def get_room_count(self, *args, **kwargs):
        req = self.rc.bind(AdminGetRoomCountRequest)  # type: AdminGetRoomCountRequest
        return self.master_is_boot() or self.auth_admin(req.jwt_token) or self.rc.ok(self.get_room_count_service.serve(req))

    def get_connected_slave(self, *args, **kwargs):
        req = self.rc.bind(AdminGetConnectedSlaveRequest)  # type: AdminGetConnectedSlaveRequest
        return self.master_is_boot() or self.auth_admin(req.jwt_token) or self.rc.ok(self.get_connected_slave_service.serve(req))

    def admin_login(self, *args, **kwargs):
        req = self.rc.bind(AdminLoginRequest)  # type: AdminLoginRequest
        return self.auth_admin(req.jwt_token) or self.rc.ok(self.admin_login_service.serve(req))

    def admin_boot_master(self, *args, **kwargs):
        req = self.rc.bind(AdminBootMasterRequest)  # type: AdminBootMasterRequest
        return self.auth_admin(req.jwt_token) or self.rc.ok(self.admin_boot_master_service.serve(req))

    def admin_shutdown_master(self, *args, **kwargs):
        req = self.rc.bind(AdminShutdownRequest)  # type: AdminShutdownRequest
        return self.master_is_boot() or self.auth_admin(req.jwt_token) or self.rc.ok(self.admin_shutdown_master_service.serve(req))

    def set_heat_mode(self, *args, **kwargs):
        # self.set_mode(*args, **kwargs)
        assert False
        pass

    def set_cool_mode(self, *args, **kwargs):
        # self.set_mode(*args, **kwargs)
        assert False
        pass

    def temp_increase(self, *args, **kwargs):
        # req.target = current_temperature + 1
        # self.set_current_temperature(*args, **kwargs)
        assert False
        pass

    def temp_decrease(self, *args, **kwargs):
        # req.target = current_temperature - 1
        # self.set_current_temperature(*args, **kwargs)
        assert False
        pass

    def metrics_delay(self, *args, **kwargs):
        req = self.rc.bind(AdminSetMetricDelayRequest) # type: AdminSetMetricDelayRequest
        return self.auth_admin(req.jwt_token) or self.rc.ok(self.set_metrics_delay_service.serve(req))

    def update_delay(self, *args, **kwargs):
        req = self.rc.bind(AdminSetUpdateDelayRequest) # type: AdminSetUpdateDelayRequest
        return self.auth_admin(req.jwt_token) or self.rc.ok(self.set_update_delay_service.serve(req))
