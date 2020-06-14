from threading import Lock
from typing import Tuple

from abstract.component import MasterAirCond, ConfigurationProvider, Configuration, MasterFanPipe
from abstract.consensus import FanSpeed, AirMode
from lib.stoppable_thread import StoppableThread


class MasterAirCondImpl(StoppableThread, MasterAirCond):

    def __init__(self, inj):
        super().__init__(lambda: None)
        cfg = inj.require(ConfigurationProvider).get()  # type: Configuration
        self.mode = AirMode(cfg.master_default.mode)  # type: AirMode
        self.default_temperature = cfg.master_default.default_temperature  # type: float
        self.cool_min, self.cool_max = cfg.master_default.cool_min, cfg.master_default.cool_max
        self.heat_min, self.heat_max = cfg.master_default.heat_min, cfg.master_default.heat_max
        self.update_delay = cfg.slave_default.update_delay
        self.metric_delay = cfg.slave_default.metric_delay
        self.mutex = Lock()  # type: Lock
        self.fan_pipe = inj.require(MasterFanPipe)  # type: MasterFanPipe
        self.is_boot = True  # type: bool


    def get_md_pair(self) -> Tuple[AirMode, float]:
        self.mutex.acquire()
        p = (self.mode, self.default_temperature)
        self.mutex.release()
        return p

    def get_delay_pair(self) -> Tuple[int, int]:
        '''
        return (update, metric) delay
        '''
        with self.mutex:
            p = (self.update_delay, self.metric_delay)
        return p


    def start_supply(self, room_id: int, speed: FanSpeed, mode: AirMode):
        self.fan_pipe.start_supply(room_id, speed, mode)

    def stop_supply(self, room_id: int):
        self.fan_pipe.stop_supply(room_id)
