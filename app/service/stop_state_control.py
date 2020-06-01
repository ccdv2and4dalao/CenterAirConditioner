from abc import abstractmethod, ABC

from abstract.service import StartStateControlService


class BaseStartStateControlServiceImpl(StartStateControlService, ABC):

    @abstractmethod
    def stop_supply(self, room_id: int):
        pass
