from abc import abstractmethod, ABC

from abstract.service import StartStateControlService
from proto import FailedResponse
from proto.start_state_control import Mode, FanSpeed, StartStateControlRequest


class BaseStartStateControlServiceImpl(StartStateControlService, ABC):

    @abstractmethod
    def check_configuration(self, req: StartStateControlRequest) -> FailedResponse or None:
        pass

    @abstractmethod
    def start_supply(self, room_id: int, mode: Mode, speed: FanSpeed, target_temperature: float):
        pass
