import enum

from proto import Request, Response


class AdminGetServerStatusRequest(Request):
    def __init__(self):
        super().__init__()
        self.jwt_token = ''  # type: str

    def bind_header(self, h):
        self.jwt_token = h['Authorization']


class ServerState(enum.Enum):
    Idle = 'idle'
    Working = 'working'
    Busy = 'busy'


class AdminGetServerStatusResponse(Response):
    def __init__(self):
        super().__init__()
        self.mode = ''  # type: str
        self.work_state = ''  # type: str
        self.current_temperature = 0.0  # type: float
        self.metric_delay = 100  # type: int
        self.update_delay = 100  # type: int
        # 使用ping方法检测服务器状态
        # self.server_state = ''  # type: str
