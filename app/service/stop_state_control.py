
from abstract.service import StopStateControlService
from app.service.state_control import BasicStateControlServiceImpl
from lib.injector import Injector
from proto import FailedResponse
from proto.stop_state_control import StopStateControlRequest, StopStateControlResponse


class StopStateControlServiceImpl(BasicStateControlServiceImpl, StopStateControlService):
    def __init__(self, inj: Injector):
        super().__init__(inj)

    def serve(self, req: StopStateControlRequest) -> StopStateControlResponse or FailedResponse:
        return self.stop_supply(req.token)

    def stop_supply(self, token: str):
        room_info = self.connection_pool.get(token)
        if room_info.need_fan:
            self.connection_pool.put_need_fan(token, False)
        self.push_stop_request(token, room_info.room_id, self.generate_tag())
        return StopStateControlResponse()
