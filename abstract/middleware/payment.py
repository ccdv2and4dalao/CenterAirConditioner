from abc import ABC, abstractmethod

from abstract.middleware.abstract import Middleware
from proto.metrics import MetricsRequest
from proto.generate_statistics import GenerateStatisticRequest
from proto.stop_state_control import StopStateControlRequest


class PaymentMiddleware(Middleware, ABC):
    """
    鉴权中间件
    """
    pass

    @abstractmethod
    def __init__(self):
        pass
