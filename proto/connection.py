from proto import Request, Response


class ConnectionRequest(Request):
    def __init__(self):
        super().__init__()
        self.id = ''  # type: str
        self.app_key = ''  # type: str

    def bind_dict(self, d: dict):
        if d is None:
            return
        self.room_id = d['room_id']
        self.id = d['id']


class ConnectionResponse(Response):
    def __init__(self):
        super().__init__()
        self.user_id = 0  # type: int
        self.room_id = 0  # type: int
        self.default_temperature = 0.0  # type: float
        self.metric_delay = 0  # type: int
        self.update_delay = 0  # type: int
        self.mode = ''  # type: str
