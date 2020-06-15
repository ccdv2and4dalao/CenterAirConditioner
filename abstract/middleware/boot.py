from abc import ABC, abstractmethod

from abstract.middleware.abstract import Middleware
from proto import MasterAirCondNotAlive
from typing import Optional

class BootMiddleware(Middleware, ABC):
    """
    开关机中间件
    """
    pass

    @abstractmethod
    def __call__(self) -> Optional[MasterAirCondNotAlive]:
        pass
