from abstract.component.jwt import JWT
from abstract.middleware.auth import AuthAdminMiddleware
from app.router.flask import RouteController
from lib.injector import Injector
from proto import AuthJWTFailed


class AuthAdminMiddlewareImpl(AuthAdminMiddleware):
    def __init__(self, inj: Injector):
        self.rc = inj.require(RouteController)  # type: RouteController
        self.jwt = inj.require(JWT)  # type: JWT

    def __call__(self, jwt_token):
        auth = self.jwt.authenticate(jwt_token)
        if isinstance(auth, Exception):
            return self.rc.err(AuthJWTFailed(f'AuthJWTFailed: {type(auth)}: {auth}'))
        return None
