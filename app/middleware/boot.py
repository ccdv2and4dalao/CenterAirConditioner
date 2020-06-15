from typing import Optional

from abstract.component.air import MasterAirCond
from abstract.middleware.boot import BootMiddleware
from proto import MasterAirCondNotAlive


class BootMiddlewareImpl(BootMiddleware):
    """
    开关机中间件
    """

    def __init__(self, inj):
        self.master_air_cond = inj.require(MasterAirCond)  # type: MasterAirCond

    def __call__(self) -> Optional[MasterAirCondNotAlive]:
        if not self.master_air_cond.is_boot:
            return MasterAirCondNotAlive("master air conditional is off")
        return None
