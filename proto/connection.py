from proto import Request, Response


class ConnectionRequest(Request):
    def __init__(self):
        super().__init__()
        self.room_id = ''  # type: str
        self.id = ''  # type: str


class ConnectionResponse(Response):
    def __init__(self):
        super().__init__()
        self.default_temperature = 0.0  # type: float
        self.metric_delay = 0  # type: int
        self.update_delay = 0  # type: int
        self.mode = ''  # type: str
