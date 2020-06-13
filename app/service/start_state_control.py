
from abstract.consensus import AirMode, FanSpeed
from abstract.service import StartStateControlService
from app.service.state_control import BasicStateControlServiceImpl
from lib.injector import Injector
from proto import FailedResponse, ConflictMode, InvalidFanSpeedValue, InvalidModeValue
from proto.start_state_control import StartStateControlRequest, StartStateControlResponse


class StartStateControlServiceImpl(BasicStateControlServiceImpl, StartStateControlService):
    def __init__(self, inj: Injector):
        super().__init__(inj)

    def serve(self, req: StartStateControlRequest) -> StartStateControlResponse or FailedResponse:
        return self.check_configuration(req) or self.start_supply(req.token, FanSpeed(req.speed), AirMode(req.mode))

    def check_configuration(self, req: StartStateControlRequest) -> FailedResponse or None:

        # noinspection PyProtectedMember
        if req.mode not in AirMode._value2member_map_:
            return InvalidModeValue(f'invalid mode enum value: {req.mode}')

        # noinspection PyProtectedMember
        if req.speed not in FanSpeed._value2member_map_:
            return InvalidFanSpeedValue(f'invalid fan_speed enum value: {req.speed}')

        current_mode = self.master_air_cond.mode.value
        if req.mode != current_mode:
            return ConflictMode(f'conflict with current mode: want {current_mode}, got {req.mode}')

        return None

    def start_supply(self, room_id: int, speed: FanSpeed, mode: AirMode) -> StartStateControlResponse or None:
        room_info = self.connection_pool.get(room_id)
        if not room_info.need_fan:
            self.connection_pool.put_need_fan(room_id, True)

        self.push_start_request(room_info.room_id, speed, mode, self.generate_tag())
        return StartStateControlResponse()


if __name__ == '__main__':
    # noinspection PyProtectedMember
    print('heat' in AirMode._value2member_map_)
    # noinspection PyProtectedMember
    print('x' in AirMode._value2member_map_)
