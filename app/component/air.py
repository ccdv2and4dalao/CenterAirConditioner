from threading import Lock
from typing import Tuple

from abstract.component import MasterAirCond, ConfigurationProvider, Configuration
from abstract.consensus import FanSpeed, AirMode
from lib.stoppable_thread import StoppableThread
from app.device import MasterAirconDeviceImpl


class MasterAirCondImpl(StoppableThread, MasterAirCond):

    def __init__(self, inj):
        super().__init__(lambda: None)
        cfg = inj.require(ConfigurationProvider).get()  # type: Configuration
        self.temp_contraint = cfg.MasterDefault.temp_contraint
        self.mode = AirMode(cfg.master_default.mode)  # type: AirMode
        self.default_temperature = cfg.master_default.default_temperature  # type: float
        self.mutex = Lock()  # type: Lock
        self.device = MasterAirconDeviceImpl()

    def get_md_pair(self) -> Tuple[AirMode, float]:
        self.mutex.acquire()
        p = (self.mode, self.default_temperature)
        self.mutex.release()
        return p

    def start_supply(self, room_id: int, speed: FanSpeed, mode: AirMode):
        pass

    def stop_supply(self, room_id: int):
        pass
