from abc import abstractmethod, ABC

from abstract.component.air import MasterAirCond
from abstract.service import StartStateControlService
from lib.injector import Injector
from proto import FailedResponse
from proto.start_state_control import Mode, FanSpeed, StartStateControlRequest


class BaseStartStateControlServiceImpl(StartStateControlService, ABC):
    def __init__(self, inj: Injector):
        self.master_air_cond = inj.require(MasterAirCond)  # type: MasterAirCond

    @abstractmethod
    def check_configuration(self, req: StartStateControlRequest) -> FailedResponse or None:
        if req.mode != self.master_air_cond.mode:
            return

    @abstractmethod
    def start_supply(self, room_id: int, mode: Mode, speed: FanSpeed, target_temperature: float):
        pass
