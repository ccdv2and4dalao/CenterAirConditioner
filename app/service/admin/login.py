import datetime

from abstract.component import ConfigurationProvider, SystemEntropyProvider
from abstract.component.jwt import JWT
from abstract.service.admin import AdminLoginService
from proto import FailedResponse, WrongPassword
from proto.admin.login import AdminLoginRequest, AdminLoginResponse


class AdminLoginServiceImpl(AdminLoginService):
    def __init__(self, inj):
        self.cfg = inj.require(ConfigurationProvider)  # type: ConfigurationProvider
        self.random_source = inj.require(SystemEntropyProvider)  # type: SystemEntropyProvider
        self.jwt = inj.require(JWT)  # type: JWT
        self.expire_time = datetime.timedelta(hours=1)

    def serve(self, req: AdminLoginRequest) -> AdminLoginResponse or FailedResponse:
        if req.admin_token != self.cfg.get().admin_config.admin_password:
            return WrongPassword()
        return AdminLoginResponse(self.jwt.create_jwt_token(
            {'exp': datetime.datetime.now() + self.expire_time, 'pd': self.random_source.get_entropy(8)}))
