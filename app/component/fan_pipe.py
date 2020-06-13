from abc import abstractmethod

from abstract.consensus import FanSpeed, AirMode


class MasterFanPipe(object):

    @abstractmethod
    def start_supply(self, room_id: int, speed: FanSpeed, mode: AirMode):
        """
        开始送风，什么模式
        由MasterAirCond调用，不是由从控调用，向从控送风
        """

    @abstractmethod
    def supply_once(self, room_id: int, duration: int):
        """
        送一次风，送了多久（毫秒）
        由MasterAirCond调用，不是由从控调用，向从控送风
        """
