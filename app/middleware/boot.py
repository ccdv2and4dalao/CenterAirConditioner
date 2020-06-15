from typing import Optional

from abstract.component.air import MasterAirCond
from app.router.flask import RouteController
from abstract.middleware.boot import BootMiddleware
from proto import MasterAirCondNotAlive

class BootMiddlewareImpl(BootMiddleware):
    """
    开关机中间件
    """
    def __init__(self, inj):
        self.master_air_cond = inj.require(MasterAirCond) # type: MasterAirCond
        self.rc = inj.require(RouteController)  # type: RouteController

    def __call__(self) -> Optional[MasterAirCondNotAlive]:
        if not self.master_air_cond.is_boot:
            return self.rc.err(MasterAirCondNotAlive("master aircon is off"))
        return None
