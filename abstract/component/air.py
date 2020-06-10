from abc import abstractmethod
from typing import Tuple

from abstract.consensus import AirMode, FanSpeed
from .bootable import Bootable


class AirCond(object):

    @abstractmethod
    def __init__(self):
        self.mode = ''
        self.current_temperature = 0.0
        # todo: ?
        self.status = {}


todo_object = object


class MasterAirCond(AirCond, Bootable):

    @abstractmethod
    def get_md_pair(self) -> Tuple[AirMode, float]:
        pass

    @abstractmethod
    def start_supply(self, room_id: int, speed: FanSpeed, mode: AirMode, target_temperature: float):
        pass

    @abstractmethod
    def stop_supply(self, room_id: int, speed: FanSpeed, mode: AirMode, target_temperature: float):
        pass
