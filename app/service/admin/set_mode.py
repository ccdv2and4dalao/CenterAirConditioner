from abstract.component import MasterAirCond
from abstract.consensus import AirMode
from abstract.service.admin.set_mode import AdminSetModeService
from proto import FailedResponse, InvalidModeValue
from proto.admin.set_mode import AdminSetModeRequest, AdminSetModeResponse


class AdminSetModeServiceImpl(AdminSetModeService):
    def __init__(self, inj):
        self.master_air_cond = inj.require(MasterAirCond)  # type: MasterAirCond

    def serve(self, req: AdminSetModeRequest) -> AdminSetModeResponse or FailedResponse:
        # noinspection PyProtectedMember
        if req.mode not in AirMode._value2member_map_:
            return InvalidModeValue(f'invalid mode enum value: {req.mode}')

        self.master_air_cond.mode = req.mode
        return AdminSetModeResponse()
