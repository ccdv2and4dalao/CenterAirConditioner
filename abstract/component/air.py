from abc import abstractmethod
from typing import Tuple

from abstract.consensus import AirMode, FanSpeed
from .bootable import Bootable


# 1.空调系统由中央空调和房间空调两部分构成；

class AirCond(object):

    @abstractmethod
    def __init__(self):
        self.mode = AirMode.Cool.value  # type: AirMode
        self.current_temperature = 0.0  # type: float
        # todo: ?
        self.status = {}


todo_object = object

# 2.中央空调是冷暖两用，根据季节进行工作模式调整。
#    a)当设置为供暖时，供暖温度控制在25°C～30°C之间；
#    b)当设置为制冷时，制冷温度控制在18°C～25°C之间。

# 3.中央空调具备开关按钮，只可人工开启和关闭，中央空调正常开启后处于待机状态。
#     a)中央空调开机后，默认处于制冷模式，缺省工作温度为22°C，当切换到供暖模式时，缺省工作温度为28°C；
#     b)当关闭后，不响应来自房间的任何温控请求；

class MasterAirCond(AirCond, Bootable):

    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass

    @abstractmethod
    def is_on(self) -> bool:
        pass

    @abstractmethod
    def get_md_pair(self) -> Tuple[AirMode, float]:
        pass

    @abstractmethod
    def start_supply(self, room_id: int, speed: FanSpeed, mode: AirMode):
        pass

    @abstractmethod
    def stop_supply(self, room_id: int):
        pass
