from abc import abstractmethod


class AirCond(object):

    @abstractmethod
    def __init__(self):
        self.mode = ''
        self.current_temperature = 0.0
        # todo: ?
        self.status = {}


class MasterAirCond(AirCond):

    @abstractmethod
    def __init__(self):
        super().__init__()
