from proto import Request, Response


class AdminGetConnectedSlaveRequest(Request):
    def __init__(self):
        super().__init__()
        self.jwt_token = ''  # type: str
        self.inc_id = 0  # type: int

    def bind_dict(self, d: dict):
        if d is None:
            return
        self.inc_id = int(d['id'])

    def bind_header(self, h):
        self.jwt_token = h['Authorization']


class AdminGetConnectedSlavesRequest(Request):
    def __init__(self):
        super().__init__()
        self.jwt_token = ''  # type: str
        self.page_number = 0  # type: int
        self.page_size = 0  # type: int

    def bind_dict(self, d: dict):
        if d is None:
            return
        self.page_number = int(d['page_number'])
        self.page_size = int(d['page_size'])

    def bind_header(self, h):
        self.jwt_token = h['Authorization']


# 按照从机所在不同房间，每个房间至少显示：房间号(从机号或IP等)、开关状态、当前温度、送风状态、当前风速
class AdminGetConnectedSlaveResponseItem(object):
    def __init__(self, inc_id: int = 0, room_id: str = '', connected=False, current_temperature=0.0, need_fan=False,
                 fan_speed=''):
        self.id = inc_id  # type: int
        self.room_id = room_id  # type: str
        self.connected = connected  # type: bool
        self.current_temperature = current_temperature  # type: float
        self.need_fan = need_fan  # type: bool
        self.fan_speed = fan_speed  # type: str


class AdminGetConnectedSlaveResponse(Response):
    def __init__(self, item: dict = None):
        super().__init__()
        self.data = item or AdminGetConnectedSlaveResponseItem().__dict__  # type: dict


class AdminGetConnectedSlavesResponse(Response):
    def __init__(self, data=None):
        super().__init__()
        self.data = data or []  # type: list
