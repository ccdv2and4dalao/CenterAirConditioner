from abc import abstractmethod

from abstract.component import Bootable


class AirCond(object):

    @abstractmethod
    def __init__(self):
        self.mode = ''
        self.current_temperature = 0.0
        # todo: ?
        self.status = {}


class MasterAirCond(AirCond, Bootable):

    @abstractmethod
    def __init__(self):
        super().__init__()
