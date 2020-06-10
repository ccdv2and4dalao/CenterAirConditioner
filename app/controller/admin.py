from abstract.component.jwt import JWT
from abstract.controller import AdminController, DaemonAdminController
from abstract.service.admin import AdminLoginService, AdminBootMasterService, AdminShutdownMasterService
from app.router.flask import RouteController
from lib.injector import Injector
from proto import AuthJWTFailed
from proto.admin.boot import AdminBootMasterRequest
from proto.admin.login import AdminLoginRequest
from proto.admin.shutdown import AdminShutdownRequest


class FlaskDaemonAdminControllerImpl(DaemonAdminController):

    def __init__(self, inj: Injector):
        self.rc = inj.require(RouteController)  # type: RouteController
        self.jwt = inj.require(JWT)  # type: JWT
        self.login_service = inj.require(AdminLoginService)
        self.boot_service = inj.require(AdminBootMasterService)
        self.shutdown_service = inj.require(AdminShutdownMasterService)

    def login(self, *args, **kwargs):
        return self.rc.ok(self.login_service.serve(self.rc.bind(AdminLoginRequest)))

    def boot(self, *args, **kwargs):
        req = self.rc.bind(AdminBootMasterRequest)  # type: AdminBootMasterRequest
        return self.auth(req) or self.rc.ok(self.boot_service.serve(req))

    def shutdown(self, *args, **kwargs):
        req = self.rc.bind(AdminShutdownRequest)  # type: AdminShutdownRequest
        return self.auth(req) or self.rc.ok(self.shutdown_service.serve(req))

    def auth(self, req):
        auth = self.jwt.authenticate(req.jwt_token)
        if isinstance(auth, Exception):
            return self.rc.err(AuthJWTFailed(f'AuthJWTFailed: {type(auth)}: {auth}'))
        return None


class FlaskAdminControllerImpl(AdminController):

    def __init__(self, _: Injector):
        pass

    def set_mode(self, *args, **kwargs):
        pass

    def set_heat_mode(self, *args, **kwargs):
        # self.set_mode(*args, **kwargs)
        pass

    def set_cool_mode(self, *args, **kwargs):
        # self.set_mode(*args, **kwargs)
        pass

    def set_current_temperature(self, *args, **kwargs):
        pass

    def temp_increase(self, *args, **kwargs):
        # req.target = current_temperature + 1
        # self.set_current_temperature(*args, **kwargs)
        pass

    def temp_decrease(self, *args, **kwargs):
        # req.target = current_temperature - 1
        # self.set_current_temperature(*args, **kwargs)
        pass

    def get_server_status(self, *args, **kwargs):
        pass
