from threading import Lock
from typing import Tuple

from abstract.component import MasterAirCond, ConfigurationProvider, Configuration
from abstract.consensus import FanSpeed, AirMode
from lib.stoppable_thread import StoppableThread


class MasterAirCondImpl(StoppableThread, MasterAirCond):

    def __init__(self, inj):
        super().__init__(lambda: None)
        cfg = inj.require(ConfigurationProvider).get()  # type: Configuration
        self.mode = AirMode(cfg.master_default.mode)  # type: AirMode
        self.default_temperature = cfg.master_default.default_temperature  # type: float
        self.mutex = Lock()  # type: Lock

    def get_md_pair(self) -> Tuple[AirMode, float]:
        self.mutex.acquire()
        p = (self.mode, self.default_temperature)
        self.mutex.release()
        return p

    def start_supply(self, room_id: int, speed: FanSpeed, mode: AirMode, target_temperature: float):
        pass

    def stop_supply(self, room_id: int, speed: FanSpeed, mode: AirMode, target_temperature: float):
        pass
