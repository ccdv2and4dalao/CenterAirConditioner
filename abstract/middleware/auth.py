from abc import ABC, abstractmethod

from abstract.middleware.abstract import Middleware
from proto import Response


class AuthAdminMiddleware(Middleware, ABC):
    """
    鉴权中间件 (管理员)
    """
    pass

    @abstractmethod
    def __call__(self, jwt_token: str) -> Response:
        pass


class AuthSlaveMiddleware(Middleware, ABC):
    """
    鉴权中间件（从控）
    """
    pass

    @abstractmethod
    def __call__(self, app_key: str) -> Response:
        pass
