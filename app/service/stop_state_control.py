from abstract.component import MasterAirCond
from abstract.service import StopStateControlService
from lib.injector import Injector
from proto import FailedResponse
from proto.stop_state_control import StopStateControlRequest, StopStateControlResponse


class StopStateControlServiceImpl(StopStateControlService):
    def __init__(self, inj: Injector):
        self.master_air_cond = inj.require(MasterAirCond)  # type: MasterAirCond

    def serve(self, req: StopStateControlRequest) -> StopStateControlResponse or FailedResponse:
        return self.stop_supply(0)

    def stop_supply(self, room_id: int):
        assert (self.master_air_cond.stop_supply(room_id) is None)
        return StopStateControlResponse()
