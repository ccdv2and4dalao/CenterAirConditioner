from abc import abstractmethod
from abstract.consensus import AirMode

class MasterAirconDevice(object):

    @abstractmethod
    def boot(self) -> bool:
        pass

    @abstractmethod
    def shutdown(self) -> None:
        pass

    @abstractmethod
    def get_target_temperature(self) -> float:
        pass

    @abstractmethod
    def get_currrent_temperature(self) -> float:
        pass

    @abstractmethod
    def get_default_temperature(self, mode: AirMode) -> float:
        pass
