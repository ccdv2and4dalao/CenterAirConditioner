from abc import ABC, abstractmethod

from abstract.middleware.abstract import Middleware


class AuthMiddleware(Middleware, ABC):
    """
    鉴权中间件
    """
    pass

    # todo: design auth middleware
    # noinspection PyUnusedLocal
    @abstractmethod
    def __init__(self, entity: str, mask: int):
        pass
