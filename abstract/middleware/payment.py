from abc import ABC, abstractmethod

from abstract.middleware.abstract import Middleware


class PaymentMiddleware(Middleware, ABC):
    """
    鉴权中间件
    """
    pass

    @abstractmethod
    def __init__(self):
        pass
