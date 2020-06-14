from abstract.component.jwt import JWT
from abstract.middleware.auth import AuthAdminMiddleware, AuthSlaveMiddleware
from app.router.flask import RouteController
from lib.injector import Injector
from proto import AuthJWTFailed, Request


class AuthAdminMiddlewareImpl(AuthAdminMiddleware):
    def __init__(self, inj: Injector):
        self.rc = inj.require(RouteController)  # type: RouteController
        self.jwt = inj.require(JWT)  # type: JWT

    def __call__(self, jwt_token):
        auth = self.jwt.authenticate(jwt_token)
        if isinstance(auth, Exception):
            return self.rc.err(AuthJWTFailed(f'AuthJWTFailed: {type(auth)}: {auth}'))
        return None


class AuthSlaveMiddlewareImpl(AuthSlaveMiddleware):
    """
    鉴权中间件（从控）
    """
    def __init__(self, inj: Injector):
        self.rc = inj.require(RouteController)  # type: RouteController
        self.jwt = inj.require(JWT)  # type: JWT

    def __call__(self, req: Request, jwt_token: str):
        auth = self.jwt.authenticate(jwt_token)
        if isinstance(auth, Exception):
            return self.rc.err(AuthJWTFailed(f'AuthJWTFailed: {type(auth)}: {auth}'))
        req.room_id = auth['room_id']
        return None
